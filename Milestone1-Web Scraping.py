from urllib.request import Request
import urllib
from datetime import datetime
import numpy as np
import pandas as pd
import csv

# sector_key_value = [{"main_market": "healthcare"}, {"main_market": "energy"}, {"main_market": "tecnology"},
#                    {"main_market": "properties"}, {"main_market": "utilities"}, {"main_market": "finance"},
#                    {"main_market": "telco_media"}, {"main_market": "consumer"}, {"main_market": "constructn"},
#                    {"main_market": "reits"}, {"main_market": "ind-prod"}, {"main_market": "plantation"},
#                    {"main_market": "transport"}, {"main_market": "specialpurposeacquis"}]
sector_key_value = [{"main_market": "tecnology"}, {"main_market": "healthcare"}, {"main_market": "properties"}]

stock_list = []
for item in sector_key_value:
    for k, v in item.items():
        stock_list.append(
            ["https://s3-ap-southeast-1.amazonaws.com/biz.thestar.com.my/json/sectors/{0}/{1}/stocks.js".format(k, v),
             k, v])


def company_name(js_urls):
    for url in js_urls:
#        try:

            res = urllib.request.urlopen(url[0])
            body = str(res.read()).split("=")
            body = body[1].replace("\\r\\n", "")
            body = body.replace(body[0:14], "")
            body = body.replace("]};\'", "")
            data = eval(body)
            try:
                for item in data:
                    crawl_data(item, url[1], url[2])
            except:
                crawl_data(data, url[1], url[2])
#        except:
#            print("error_stop1")
#            continue


def crawl_data(name, sector, subsector):
    start_date = "1546376400"
    end_date = "1577826000"
    url = "https://charts.thestar.com.my/datafeed-udf/history?symbol={0}&resolution=D&from={1}&to={2}".format(name["counter"], start_date, end_date)
    res = urllib.request.urlopen(url)
    body = res.read().decode()
    dict_data = eval(body)
#    print(dict_data)
    df=pd.DataFrame(dict_data)

    csv_file = format(name["counter"])+".csv"
    df.to_csv (csv_file, index = False, header=True)

if __name__ == "__main__":
    company_name(stock_list)