from encodings import utf_8
from re import A
import requests
import json
import pandas
import time


url = "https://0.zone/api/data/"
headers = {
    'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
    'Content-Type': 'application/json;charset=UTF_8',
    'Content-Length': ''
}


#ab模式二进制追加
logfile=open("log.txt","ab",buffering=0)
alldf=pandas.DataFrame(columns = ['pagenum', 'ip', 'port', 'url', 'title', 'os', 'ping', 'cms',
       'banner_os', 'component', 'area', 'city', 'continent', 'country',
       'device_type', 'lang', 'lang_version', 'latitude', 'longitude',
       'operator', 'protection', 'protocol', 'province', 'service', 'versions',
       'extra_info', 'app_name', 'app_version', 'app_brand', 'banner',
       'html_banner', 'accuracy', 'group', 'company', 'tags',
       'icon_md5_base64', 'counterfeit', 'status_code', 'risk_score',
       'url_directory', 'parse_ip', 'toplv_domain', 'server_name',
       'server_version', 'server_brand', 'os_name', 'os_version', 'os_brand',
       'framework_name', 'framework_version', 'framework_brand',
       'js_framework_name', 'js_framework_version', 'js_framework_brand',
       'explore_timestamp', 'timestamp'])

#startpage从1开始
startpage=1
while True:
    payload = {
        "title": "XXXX有限公司",
        "title_type": "site",
        "page": startpage,
        "pagesize": 40,
        "zone_key_id": "xxxxxx"
    }
    print("[*]正在读取第{0}页!".format(startpage))
    try:
        response = requests.request("POST", url,headers=headers, data=json.dumps(payload).encode('utf-8'))

    except:
        print('[*]读取第{0}页错误!'.format(startpage))
        logfile.write("[{0}]:第 {1} 读取错误!".format(time.strftime('%Y-%m-%d %H:%M:%S'),startpage).encode('utf-8')+b"\n")
        break

    try:
        df = pandas.read_json(response.text,lines=True)
        #df等于0则返回失败
        if(df.at[0,'code']):
            print('[*]入库第{0}页错误!'.format(startpage))
            logfile.write("[{0}]:第 {1} 入库错误1!".format(time.strftime('%Y-%m-%d %H:%M:%S'),startpage).encode('utf-8')+b"\n")
            break
        
        df1 = pandas.DataFrame(df.at[0,'data'])
        if df1.empty:
            print('[*]获取第{0}页错误，数据为空!'.format(startpage))
            logfile.write("[{0}]:第 {1} 页入库错误，数据为空!".format(time.strftime('%Y-%m-%d %H:%M:%S'),startpage).encode('utf-8')+b"\n")
            break
        
        df1.insert(0,"pagenum",startpage)
    except:
        print('[*]入库第{0}页错误!'.format(startpage))
        logfile.write("[{0}]:第 {1} 入库错误2!".format(time.strftime('%Y-%m-%d %H:%M:%S'),startpage).encode('utf-8')+b"\n")
        break
    
    #alldf=pandas.concat([alldf,df1])
    #实时写入文件无延迟
    # df1.to_excel('my_excel_saved{0}.xlsx'.format(startpage), index=False)
    alldf=pandas.concat([alldf,df1])
    alldf.to_excel('my_excel_saved.xlsx', index=False)
    logfile.write("[{0}]:第 {1} 页面入库成功!".format(time.strftime('%Y-%m-%d %H:%M:%S'),startpage).encode('utf-8')+b"\n")
    
    startpage=startpage+1


logfile.close()