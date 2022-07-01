import tldextract
import pandas as pd
import time

global ALLDOMAINLEN
#设定子域名最大出现次数
DOMAIN_COUNT_MAXNUM=200

t = time.time()


#根据域名提取主域
def ExtractRootDomain(url):
    try:
        return tldextract.extract(url).domain
    except:
        return None
    finally:
        global ALLDOMAINLEN
        ALLDOMAINLEN=ALLDOMAINLEN-1
        print('\r正在提取主域,待提取数量:'+str(ALLDOMAINLEN), end='', flush=True)

alldomain_df = pd.read_csv('alltargets.txtls',header=None)
ALLDOMAINLEN =len(alldomain_df)
#插入最后一列，因txt只有一列所以固定插入第二列
alldomain_df.insert(1,"rootdomain",None)
alldomain_df.columns = ['domain','rootdomain']
#提取domain列中的主域名，赋值给rootdomain列
alldomain_df['rootdomain'] = alldomain_df.apply(lambda x: ExtractRootDomain(x.domain), axis = 1)
print('\n提取成功')

print('tiquoktime:', time.time() - t)
#计算rootmain每个值出现的次数，不用排序，并转换成df
rootdomain_counts_df=alldomain_df['rootdomain'].value_counts(sort=False).to_frame()
#只保留rootmain出现次数小于DOMAIN_COUNT_MAXNUM的行
domain_less_df=alldomain_df.loc[alldomain_df['rootdomain'].isin(rootdomain_counts_df.loc[rootdomain_counts_df['rootdomain']<DOMAIN_COUNT_MAXNUM].index.values)]
print(domain_less_df['domain'])

domain_less_df['domain'].to_csv('ok.txt',index=False)
print('初始文件长度'+str(len(alldomain_df))+'，提取主域名出现次数大于'+str(DOMAIN_COUNT_MAXNUM)+'的值域名后文件长度为:'+str(len(domain_less_df['domain'])))


print('alltime:', time.time() - t)