import pandas as pd
from lxml import etree
import requests
import tldextract

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
bing = 'https://cn.bing.com/search?q='


def school_domain(name):

    bingurl=bing+name
    req = requests.get(bingurl,headers=headers)
    tree=etree.HTML(req.text)
    res=tree.xpath('//div[@class="b_caption"]/div/cite/text()')
    
    for i in res:
        retdomain=''
        if "edu.cn" in i:
            retdomain=str(tldextract.extract(i).fqdn)
            break
    return retdomain


df=pd.read_excel("result.xlsx")
df['域名']=''
for index, row in df.iterrows():
    df.loc[index,'域名']=school_domain(row["单位"])
    print(str(index+1)+"/"+str(len(df))+"-----"+"正在查询"+row["单位"],end="\r",flush=True)

df.to_excel('domainresult.xlsx', sheet_name='Sheet1',header=True,index=None)