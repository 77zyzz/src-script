# coding: utf-8 
import pandas as pd

newdf=pd.DataFrame(columns = ['单位'])
#page为一共多少页
page=195

for i in range(1,page+1):
    url = 'https://src.sjtu.edu.cn/rank/firm/?page={}'.format(i)
    df=pd.read_html(url,encoding='utf-8',header=0)[0]
    newdf = pd.concat([newdf,df])
    print("正在爬取第"+str(i)+"页",end="\r", flush=True)


newdf.to_excel('result.xlsx', sheet_name='Sheet1',header=True,index=None)
