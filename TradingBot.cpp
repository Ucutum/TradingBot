#include <iostream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>
#include <cmath>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <fstream>
#include <thread>

using namespace std;
using ll = long long;
using dl = long double;
const ll INF = 3e18;
const ll MinCompLen = 10;
const dl eps = 1e-15;
const ll MSIZE = 5000;

struct candle {
    dl open, close, low, high, mid;
    candle(dl mid = 0) : open(mid), close(mid), low(mid), high(mid), mid(mid) {}
    candle(dl open, dl close, dl low, dl high) : open(open), close(close), low(low), high(high), mid((open + close + low + high) / 4) {}
};

using graph = vector<candle>;

vector<graph> companies;
vector<string> company_names;

void load_data(string name) {
    fstream fin(name);
    graph g;
    string s;
    getline(fin, s);
    s.push_back(';');
    ll ncnt = 0;
    string curs = "";
    for (auto sym : s) {
        if (sym == ';') {
            if (curs == "close") break;
            curs = "";
            ncnt++;
            continue;
        }
        if (sym >= 'A' && sym <= 'Z') sym = 'a' + (sym - 'A');
        curs.push_back(sym);
    }
    while (getline(fin, s)) {
        ll cnt = 0;
        string num = "";
        for (auto sym : s) {
            if (sym == ' ') continue;
            if (sym == ',') sym = '.';
            if (cnt == ncnt && sym != ';') num.push_back(sym);
            if (sym == ';') cnt++;
        }
        if (num.empty()) continue;
        g.push_back(stod(num));
    }
    //reverse(g.begin(), g.end());
    companies.push_back(g);
}

ll g1 = 0, b1 = 0;

struct tradeBot {
    dl aggressiveness = 1;
    string username;
    string exchange;
    dl balance = 0;
    dl summary = 0;
    dl commission = 0.0000;
    ll company_count = 0;
    ll min_trend_size = 6;
    ll max_trend_size = 60;
    vector<dl> share_count;
    vector<dl> cur_max;
    vector<dl> fall_size;
    vector<ll> delay;

    //a
    vector<dl> buy_cost;

    ll del = 15;
    ofstream ad_fout; //= ofstream("gdata/Advice.txt");
    ll curtime = 2200;
    ll bought = 0;
    ll mxcnt = 10;
    bool on_screen = true;

    void save_package() {
        ofstream pack_fout = ofstream("gdata/Package_" + exchange + ".txt");
        pack_fout << "MONEY " << balance << endl;
        for (ll i = 0; i < company_count; i++) {
            pack_fout << company_names[i] << " " << share_count[i] << endl;
        }
    }

    tradeBot(dl aggressiveness = 1, dl commission = 0.0005) : aggressiveness(aggressiveness), commission(commission) {
        company_count = companies.size();
        share_count.resize(company_count);
        cur_max.resize(company_count);
        fall_size.resize(company_count);
        delay.resize(company_count);
        buy_cost.resize(company_count);

        ifstream fin("exchangeName.txt");
        fin >> exchange;

        ad_fout = ofstream("gdata/Advice_" + exchange + ".txt");
    }

    void sell(ll id) {
        balance += share_count[id] * companies[id][companies[id].size() - 1 - curtime].close * ((dl)1 - commission);
        share_count[id] = 0;
        cur_max[id] = 0;
        fall_size[id] = 0;

        dl cst = companies[id][companies[id].size() - 1 - curtime].close;
        if (cst > buy_cost[id]) g1++;
        else b1++;

        if (on_screen) cout << "SELL ALL of " << company_names[id] << endl;
        else {
            cout << "SELL ALL of " << company_names[id] << endl;
            ad_fout << company_names[id] << " -" << share_count[id] << endl;
        }
    }

    void buy(ll id, dl cost, dl fall_sz) {
        cost *= (1 - (dl)commission);
        if (cost < 1e-15) return;
        dl cnt = cost / companies[id][companies[id].size() - 1 - curtime].close;
        cnt = (ll)cnt;
        if ((ll)cnt == 0) return;
        share_count[id] += cnt;
        buy_cost[id] = companies[id][companies[id].size() - 1 - curtime].close;
        balance -= cnt * companies[id][companies[id].size() - 1 - curtime].close * ((dl)1 + commission);
        cur_max[id] = companies[id][companies[id].size() - 1 - curtime].close;
        fall_size[id] = fall_sz;
        if (on_screen) cout << "BUY " << cnt << " shares of " << company_names[id] << endl;
        else {
            cout << "BUY " << cnt << " shares of " << company_names[id] << endl;
            ad_fout << company_names[id] << " " << cnt << endl;
        }
    }

    void make() {
        for (ll i = 0; i < company_count; i++) {
            dl cur = companies[i][companies[i].size() - 1 - curtime].close;
            if (share_count[i] > 0) {
                cur_max[i] = max(cur_max[i], cur);
                dl cur_fall = cur_max[i] / cur;
                if (cur_fall > fall_size[i] + eps || companies[i][companies[i].size() - 1 - curtime].close / companies[i][companies[i].size() - 2 - curtime].close < 0.95) {
                    sell(i);
                    delay[i] = del;
                }
            }
        }
        vector<dl> trend_strength(company_count);
        vector<dl> max_trend_fall(company_count);
        vector<pair<pair<dl, dl>, ll>> vc;
        dl sum = 0;
        for (ll i = 0; i < company_count; i++) {
            if (share_count[i] > 0) continue;
            else if (delay[i] > 0) {
                delay[i]--;
                continue;
            }
            dl cur = companies[i][companies[i].size() - 1 - curtime].close;
            dl cur_min = cur;
            dl max_fall = 1;
            dl strength = 0;
            dl mx_str_fall = 0;
            dl cur_max = cur;
            for (ll t = companies[i].size() - 1 - curtime - 1; t >= 0; t--) {
                cur_min = min(cur_min, companies[i][t].close);
                cur_max = max(cur_max, companies[i][t].close);
                dl cur_fall = companies[i][t].close / cur_min;
                max_fall = max(max_fall, cur_fall);
                
                dl cur_up = (cur / companies[i][t].close - 1) * 100;
                dl cur_strength = (cur_up) / ((max_fall - 1) * 100 + aggressiveness);
                cur_strength *= ((cur / cur_max) - 0.9) * 10;
                if ((cur_strength > strength || cur_strength == strength && max_fall < mx_str_fall) && companies[i].size() - 1 - curtime - t > min_trend_size) {
                    strength = cur_strength;
                    mx_str_fall = max_fall;
                }
                if (companies[i].size() - 1 - curtime - t > max_trend_size) break;
            }
            if (strength > 5) {
                vc.push_back({ {strength, 1 + (mx_str_fall - 1) * 2 + 0.01}, i });
            }
        }
        ll c = mxcnt;
        for (ll i = 0; i < company_count; i++) {
            c -= share_count[i] > 0;
        }
        if (!vc.empty()) {
            sort(vc.rbegin(), vc.rend());
            dl sum = 0;
            for (ll i = 0; i < min((ll)vc.size(), (ll)c); i++) {
                trend_strength[vc[i].second] = vc[i].first.first * vc[i].first.first;
                max_trend_fall[vc[i].second] = vc[i].first.second;
                sum += trend_strength[vc[i].second];
            }
            dl b0 = balance;
            for (ll i = 0; i < company_count; i++) {
                if (trend_strength[i] == 0) continue;
                dl cost = (trend_strength[i] / sum) * b0;
                dl part = cost / summary;
                //if (part > 0.9) part = 0.9;
                cost = part * summary;
                buy(i, cost, max_trend_fall[i]);
            }
        }
        summary = balance;
        for (ll i = 0; i < company_count; i++) {
            summary += companies[i][companies[i].size() - 1 - curtime].close * share_count[i];
        }
    }

    void push(dl c) {
        balance += c;
        summary += c;
    }

    void save_data() {
        ofstream fout("gdata/balance_" + exchange);
        fout << balance;
        for(ll i = 0; i < company_count; i++){
            fout = ofstream("gdata/" + company_names[i] + "_" + exchange);
            fout << share_count[i] << endl;
            fout << cur_max[i] << endl;
            fout << fall_size[i] << endl;
            fout << delay[i] << endl;
        }
    }

    void load_data() {
        ifstream fin("gdata/balance_" + exchange);
        fin >> balance;
        for (ll i = 0; i < company_count; i++) {
            fin = ifstream("gdata/" + company_names[i] + "_" + exchange);
            fin >> share_count[i];
            fin >> cur_max[i];
            fin >> fall_size[i];
            fin >> delay[i];
        }
        summary = balance;
        for (ll i = 0; i < company_count; i++) {
            summary += companies[i][companies[i].size() - 1].close * share_count[i];
        }
    }
};

ofstream fff("A.csv");

void simulate(ll day0) {
    tradeBot tb(0.4, 0.0005);
    tb.push(100000);
    //tb.load_data();
    tb.curtime = day0;
    ll msizer = INF;
    for (ll i = 0; i < companies.size(); i++) msizer = min(msizer, (ll)companies[i].size());
    ll day = 1;
    for (ll i = 0; tb.curtime >= 0; i++) {
        cout << "day " << day << " : " << tb.summary << endl;
        fff << (ll)(((tb.summary / 100000) - 1) * 10000) << endl;
        tb.make();
        tb.curtime--;
        day++;
        //Sleep(300);
    }
    //tb.save_data();
    cout << "good : " << g1 << endl;
    cout << "bad : " << b1 << endl;
}

void help() {
    tradeBot tb(0.4, 0.0005);
    tb.on_screen = false;
    //tb.push(100000);
    tb.load_data();
    tb.curtime = 0;
    tb.make();
    tb.save_data();
    tb.save_package();
}

void rebuild(ll money) {
    tradeBot tb(0.4, 0.0005);
    tb.on_screen = false;
    tb.push(money);
    tb.save_data();
    tb.save_package();
}

int main() {
    cout << fixed;
    cout.precision(2);
    string foldername = "graphs";
    ifstream fin("all.csv");
    string s;
    while (getline(fin, s)) {
        if (s == "ext") break;
        string s2 = "";
        bool ww = false;
        for (auto sym : s) {
            if (ww && sym >= 'A' && sym <= 'Z') s2.push_back(sym);
            if (sym == ';') ww = true;
        }
        load_data(foldername + "/" + s2 + ".csv");
        company_names.push_back(s2);
    }

    //simulate(20);
    rebuild(1000000);   //раскоментировать - prepareFiles
    help();             //раскоментировать - redistribute
}