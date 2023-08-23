# -*- coding: utf-8 -*-
import os
import datetime
import csv
import urllib.request
from bs4 import BeautifulSoup

#HTMLで取得した文字情報をfloat型に変換する関数を定義する
#また、「///」といった文字情報を0に変換する関数を定義する
def str2float(weather_data):
    try:
        return float(weather_data)
    #例外処理：float型でreturnすることができなかった場合は0をreturn
    except:
        return 0
    
#もし受け取った文字情報に記号が含まれていた場合（数値型の場合）
def del_sym(weather_data):
    weather_data_dic = {')':'',']':'','*':''}
    #通常な処理
    try:
        if weather_data in ['--',0,0.0,'0+']:
            return float(0)
        elif weather_data in ['×','///','','#','＠',None]:
            return ''
        
        #もしweather_dataの中に「）,],*」が含まれていたらなくす
        elif weather_data in weather_data_dic:
            weather_data = weather_data.replace(weather_data,weather_data_dic[weather_data])
            return float(weather_data)
    
        #上記のif文どれにも当てはまらなかったら、float型にしたweather_dataを返す
        else:
            return float(weather_data)
        
    #最後のelseでfloat型に変換できない文字情報だったら0を返す
    except:
        return ''
    
#風向は数値ではない為、文字列を返す関数を定義する
def wind(weather_data):
    #通常な処理
    try:
        #空白はNoneで返す
        if weather_data in ['--','×','///','','#','@',None]:
            return ''
        
        #もしweather_dataの中に「）」が含まれていたら「）」をなくす
        elif ')' in weather_data:
            weather_data = weather_data.replace(')','')
            return weather_data
        
        #もしweather_dataの中に「]」が含まれていたら「]」をなくす
        elif ']' in weather_data:
            weather_data = weather_data.replace(']','')
            return weather_data
        
        #もしweather_dataの中に「*」が含まれていたら「*」をなくす
        elif '*' in weather_data:
            weather_data = weather_data.replace('*','')
            return weather_data
        
        #上記のif文どれにも当てはまらなかったら、weather_dataを返す
        else:
            return weather_data
    
    #最後のelseでエラーが起こったら
    except:
        return ''


def output_csv(prec_no,block_no,year,month):
    url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?"\
          "prec_no=%d&block_no=%d&year=%d&month=%d&day=&view="%(prec_no,block_no,year,month)
    print(url)
    data_per_month = scraping(prec_no,block_no,url,year,month)
    return data_per_month

#気象庁のデータを取得してくる関数
def scraping(prec_no,block_no,url,year,month):
    
    #urlをopenする
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    trs = soup.find("table",{"class":"data2_s"})
    
    data_list = []
    data_list_per_day = []
    
    #tableタグの中身を取得する
    #４番目以降のtrタグを取得する(４番目からスタート（0,1,2,3,4）)
    for tr in trs.findAll('tr')[4:]:
        tds = tr.findAll('td')
        #print(tds)
        
        data_list.append(prec_no)  #都府県振興局番号
        data_list.append(block_no) #観測所番号
        #scraping関数の引数で受け取ったdateをリストに格納する
        data_list.append(str(year) + "/" + str(month).zfill(2) + "/" + str(tds[0].string).zfill(2)) #年月日、日にちは０番目のtdタグの文字情報を取得する
        data_list.append(del_sym(tds[1].string)) #現地平均気圧（hPa）
        data_list.append(del_sym(tds[2].string)) #海面平均気圧（hPa）
        data_list.append(del_sym(tds[3].string)) #合計降水量（mm）
        data_list.append(del_sym(tds[4].string)) #1時間最大降水量（mm）
        data_list.append(del_sym(tds[5].string)) #10分間最大降水量（mm）
        data_list.append(del_sym(tds[6].string)) #平均気温（℃）
        data_list.append(del_sym(tds[7].string)) #最高気温（℃）
        data_list.append(del_sym(tds[8].string)) #最低気温（℃）
        data_list.append(del_sym(tds[9].string)) #平均湿度（％）
        data_list.append(del_sym(tds[10].string)) #最小湿度（％）
        data_list.append(del_sym(tds[11].string)) #平均風速（m/s）
        data_list.append(del_sym(tds[12].string)) #最大風速（m/s）
        data_list.append(wind(tds[13].string)) #最大風速風向
        data_list.append(del_sym(tds[14].string)) #最大瞬間風速(m/s)
        data_list.append(wind(tds[15].string)) #最大瞬間風速風向
        data_list.append(del_sym(tds[16].string)) #日照時間（h）
        data_list.append(del_sym(tds[17].string)) #合計降雪（cm）
        data_list.append(del_sym(tds[18].string)) #最深積雪値（cm）
        data_list.append(tds[19].string) #天気概況昼（06:00-18:00）
        data_list.append(tds[20].string) #天気概況夜（18:00-翌日06:00）
        
        data_list_per_day.append(data_list)
        #print(data_list)
        data_list=[]
    
    #一か月分の全データが格納された配列を返す
    #print(data_list_per_day)
    return data_list_per_day

def create_csv():
    #csv出力ディレクトリ
    output_dir = r"ディレクトリ"
    #出力ファイル名
    output_file = "weather_per_day2.csv"
    #csvの列名
    fields = ["都府県振興局番号","観測所番号","年月日","現地平均気圧（hPa）","海面平均気圧（hPa）","合計降水量（mm）","1時間最大降水量（mm）","10分間最大降水量（mm）",
             "気温平均（℃）","最高気温（℃）","最低気温（℃）","平均湿度（%）","最小湿度（%）","平均風速（m/s）","最大風速（m/s）","最大風速風向",
             "最大瞬間風速(m/s)","最大瞬間風速風向","日照時間（h）","合計降雪（cm）","最深積雪値（cm）","天気概況昼（06:00-18:00）","天気概況夜（18:00-翌日06:00）"]
    
    with open(os.path.join(output_dir,output_file),'w') as f:
        writer = csv.writer(f,lineterminator = '\n')
        #ヘッダをcsvに書き込む
        writer.writerow(fields)
        
        #csvファイルにデータを書き込む
        for year in range(2021,2022): #2021年のデータを取得する
            for month in range(1,13):
                for prec_no in [33]:
                    for block_no in [47584]:
                        #returnでかえってきたものは変数に入れる必要がある
                        data_per_month = output_csv(prec_no,block_no,year,month)
                        for dpd in data_per_month:
                            writer.writerow(dpd)
                                
                                
create_csv()