const getData = async () => {
    const Widget = document.querySelector("#widget");
    const res = await fetch('../../graphs/' + Widget.dataset.token + ".csv");
    const resp = await res.text();
    //   console.log(resp);
    const cdata = resp.split('\n').map((row) => {
      const [time1, open, high, low, close, volume] = row.split(';');
      return {
        time: new Date(`${time1}`).getTime() / 1000,
        open: open * 1,
        high: high * 1,
        low: low * 1,
        close: close * 1,
        volume: volume * 1,
      };
    });
    cdata.shift();
    cdata.pop();
    return cdata;
    //   console.log(cdata);
  };
  
  // getData();
  
  const displayChart = async () => {
    const chartProperties = {
      width: 1000,
      height: 400,
      timeScale: {
        timeVisible: true,
        secondsVisible: true,
      },
    };
  
    const domElement = document.getElementById('widget');
    const chart = LightweightCharts.createChart(domElement, chartProperties);
    const candleseries = chart.addCandlestickSeries();
    const klinedata = await getData();
    candleseries.setData(klinedata);
  };
  
  displayChart();