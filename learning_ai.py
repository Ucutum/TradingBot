# -*- coding: utf-8 -*-
"""Trading4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SKqkUJeJpH4wH-ftWsZAgRCpGl6_pHfu
"""
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential, load_model
from keras.initializers import RandomUniform
from keras.callbacks import History
import matplotlib.pyplot as plt
import pandas as pd
import math
from csv_parser import parse
import csv
import datetime


def read_data(filename, delimiter='\t'):
    data = pd.read_csv(filename, delimiter=delimiter)
    # Date;Open;High;Low;Close;Adj Close;Volume
    data.rename(columns={
        "Date": "<DATE>", "Open": "<OPEN>",
        "High": "<HIGH>", "Low": "<LOW>", "Close": "<CLOSE>", "Volume": "<VOL>"}, inplace=True)
    data = data[['<DATE>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
    data['<DATE>'] = pd.to_datetime(data['<DATE>'], format='%Y-%m-%d')
    data['<OPEN>'] = pd.to_numeric(data['<OPEN>'])
    data['<HIGH>'] = pd.to_numeric(data['<HIGH>'])
    data['<LOW>'] = pd.to_numeric(data['<LOW>'])
    data['<CLOSE>'] = pd.to_numeric(data['<CLOSE>'])
    data['<VOL>'] = pd.to_numeric(data['<VOL>'])
    # data.rename(columns={}, inplace=True)
    # data.set_index('Date', inplace=True)
    data.rename(columns={
        '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>': 'Close',
        '<VOL>': 'Volume', "<DATE>": "Date"}, inplace=True)
    return data


def slice_to_sections(data, x_sections_cnt, y_sections_cnt):
  sections_cnt = x_sections_cnt + y_sections_cnt
  section_count = len(data) // (sections_cnt)
  xs = []
  for i in range(x_sections_cnt):
    xs.append(data[i::sections_cnt])
  ys = []
  for i in range(x_sections_cnt, x_sections_cnt + y_sections_cnt):
    ys.append(data[i::sections_cnt])
  min_section_size = min(min([len(i) for i in xs]), min(len(i) for i in ys))
  for i in range(x_sections_cnt):
    xs[i] = xs[i][:min_section_size]
  for i in range(y_sections_cnt):
    ys[i] = ys[i][:min_section_size]
  return xs, ys


def unification(xs, ys):
  y = np.array(ys).T
  x = np.array(xs).T
  return x, y


def pack(m1, m2):
  return np.column_stack((m1, m2))


def unpack(h):
  # print("h", h)
  # print("out", np.hsplit(h, 2))
  return np.hsplit(h, 2)


def grounding(xs, ys, s=1):
  mnx = np.min(xs, axis=1)[:, np.newaxis]
  mxx = np.max(xs, axis=1)[:, np.newaxis]
  x = (xs - mnx) / (mxx - mnx)
  y = (ys - mnx) / (mxx - mnx)
  h = pack(mnx, mxx)
  return x, y, h


def grounding_one(xs, s=1):
  mnx = np.min(xs, axis=1)[:, np.newaxis]
  mxx = np.max(xs, axis=1)[:, np.newaxis]
  x = (xs - mnx) / (mxx - mnx)
  h = pack(mnx, mxx)
  return x, h


def ungrounding(x, y, mxx, s=1):
  mnx, mxx = unpack(mxx)
  xs = x * (mxx - mnx) + mnx
  ys = y * (mxx - mnx) + mnx
  return xs, ys

def ungrounding_one(x, mxx, s=1):
  mnx, mxx = unpack(mxx)
  xs = x * (mxx - mnx) + mnx
  return xs


def generate(data, x_sections_cnt, y_sections_cnt):
  gx, gy, gmxx = [], [], []
  for swp in range(x_sections_cnt):
    x, y = slice_to_sections(data[swp:], x_sections_cnt, y_sections_cnt)
    x, y = unification(x, y)
    x, y, mxx = grounding(x, y, 1)
    gx.extend(x)
    gy.extend(y)
    # print(gy)
    gmxx.extend(mxx)
  print(len(gx), len(gy), len(gmxx))
  minlen = min(len(gx), len(gy), len(gmxx))
  print(minlen)
  gx = gx[:minlen]
  gy = gy[:minlen]
  gmxx = gmxx[:minlen]
  return np.array(gx), np.array(gy), np.array(gmxx)


def make_selections(x, y, pl, mxx):
  pt = 100 - pl
  indicesl = np.random.permutation(len(x))
  x = x[indicesl]
  y = y[indicesl]
  mxx = mxx[indicesl]

  xs = min(len(x), round((len(x) * pl) // 100))
  xl = x[:xs]
  mxxl = mxx[:xs]
  xt = x[xs:]
  mxxt = mxx[xs:]

  ys = min(len(y), round((len(y) * pl) // 100))
  yl = y[:ys]
  yt = y[ys:]

  return xl, xt, yl, yt, mxxl, mxxt


def check(model, data, path, pathtxt, token):
  print("Testing model")
  pr = 1 - 0.15

  history = []
  c = 100
  test_range = range(100, len(data) - 1)
  for i in test_range:
    print(i)
    x = np.array(data[i - 100:i])
    xg, mxx = grounding_one(np.array([x]))
    p = ungrounding_one(model.predict(xg), mxx)[0]
    y = np.array([data[i]])
    # print(f"x {x[-1]} p {p[0]} y {y[0]}")
    up = c / x[-1] * p[0]
    rup = c / x[-1] * y[0]
    down = c * x[0] / p[-1]
    rdown = c * x[0] / y[-1]
    if up > down:
      c = rup
    else:
      c = rdown
    history.append(c)


  print("Прибыль при тестировании: ", history[-1])
  with open(pathtxt, "w") as f:
    f.write(f"{history[-1]}" + "\n")
  # print(len(test_range))
  plt.plot(history)
  plt.title('График прибыли')
  plt.xlabel('Время')
  plt.ylabel('Прибыль')
  plt.savefig(path)
  print("End testing")


def learn(token, foldername, fromfoldername):
  print(f"Обработка {token}")
  data = read_data(fromfoldername + token + ".csv", delimiter=';')
  print(data.head(3))
  data = data[["Close"]]
  data = np.array(data)
  data = data.T[0]
  print(len(data))
  test_data = data[-230:]
  data = data[:-230]
  xt, yt, mxxt = generate(test_data, 100, 1)
  xl, yl, mxxl = generate(data, 100, 1)
  print(len(mxxl), len(mxxt))
  model = tf.keras.models.Sequential()
  model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
  model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
  model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))
  model.compile(
      optimizer='adam', loss='mse', metrics='mse')
  history = History()
  model.fit(xl, yl, epochs=200, callbacks=[history])

  model_name = foldername + token + "_model.h5"
  model.save(model_name)
  plt.plot(history.history['loss'])
  plt.title('График сходимости')
  plt.xlabel('Эпоха')
  plt.ylabel('Функция потерь')
  plt.savefig(foldername + token + '_convergence.png')
  plt.close()

  i_stat = range(len(xt))
  loss_stat = (ungrounding_one(yt, mxxt) - ungrounding_one(model.predict(xt), mxxt))[:, 0]
  y_stat = sum(ungrounding_one(yt, mxxt)[:, 0])
  p_stat = sum(ungrounding_one(model.predict(xt), mxxt)[:, 0])
  y_diff = np.array([np.sum(np.abs(np.diff(arr))) for arr in ungrounding_one(yt, mxxt)])
  loss_for_graph = np.array([np.sum(np.abs(arr)) for arr in ungrounding_one(yt, mxxt) - ungrounding_one(model.predict(xt), mxxt)])
  y_diff_cnt, _ = np.histogram(y_diff, bins=np.arange(0, len(loss_for_graph) + 1))
  combined = zip(y_diff, loss_for_graph, y_diff_cnt)
  sorted_combined = sorted(combined, key=lambda x: x[0])
  y_diff, loss_for_graph, y_diff_cnt = zip(*sorted_combined)
  plt.scatter(y_diff, loss_for_graph, cmap='viridis', alpha=0.7, s=0.5)
  plt.xlabel('diff')
  plt.ylabel('loss')
  plt.title('Scatter Plot of y vs p with Color-encoded Loss')
  plt.savefig(foldername + token + '_loss.png')
  plt.close()

  check(model, test_data, foldername + token + '_check.png',
          foldername + token + 'result.txt', token)


def main():
  with open("all.csv") as f:
    companies = [e[1] for e in csv.reader(f, delimiter=";")]
  companies = [companies[-1]]
  for c in companies:
    print(f"Learning {c}")
    learn(c, "models/", "graphs/")


def main_check():
  model = load_model("models/NVDA_model.h5")
  data = read_data("graphs/NVDA.csv", delimiter=';')
  # data = data[["Open", "Close"]].mean(axis=1)
  data = data[["Close"]]
  data = np.array(data)
  test_data = data[-130:]
  check(model, test_data, "models/NVDA_check.png")


if __name__ == '__main__':
  main()