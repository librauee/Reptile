# 高可用代理IP

## Source
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/代理IP/ip.png)
* [仓库链接](https://github.com/dxxzst/free-proxy-list)
* 该仓库提供了免费的ip代理，可用性和实时性都可以接受


## Target
* 爬取该repo上的代理IP列表，进行筛选并验证IP的可用性
* getgoodip.py
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/代理IP/download.png)

## Tips
* http://ip.tool.chinaz.com/ 是校验IP的网站
* 如何使用：

```python

conn=MongoClient('127.0.0.1', 27017)      
db=conn.proxy
mongo_proxy=db.good_proxy
proxy_data=mongo_proxy.find()
proxies=json_normalize([ip for ip in proxy_data])
proxy_list=list(proxies['ip'])
proxy=random.choice(proxy_list)
r=requests.get(url,headers=headers,proxies={'https': 'https://{}'.format(proxy),'http':'http://{}'.format(proxy)})

```
 
