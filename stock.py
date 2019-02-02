Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 17:26:49) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import re
>>> import requests
>>> import traceback
>>> from bs4 import BeautifulSoup
>>> def getHTMLText(url,code='utf8'):
	try:
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		r.encoding=code
		return r.text
	except:
		print("")

		
>>> def getStockList(lst,stockURL):
	html=getHTMLText(stockURL)
	soup=BeautifulSoup(html,'html.parser')
	a=soup.find_all('a')
	for i in a:
		try:
			href=i.attrs['href']
			lst = append(re.findall(r"[s][hz]\d{6}", href)[0])
		except:
			continue

		
>>> def getStockInfo(lst,stockURL,fpath):
	count=0
	for stock in lst:
		url=stockURL+stock+".html"
		html = getHTMLText(url)
		try:
			if html=="":
				continue
			infoDict = {}
			soup=BeautifulSoup(html,'html.parser')
			stockInfo=soup.find('div',attrs={'class':'stocks-bets'})
			infoDict.update({'股票名称':name.text.split()[0]})
			keyList=stockInfo.find_all('dt')
			valueList=stockInfo.find_all('dd')
			for i in range(len(ketList)):
				key=keyList[i].text
				val=valueList[i].text
				infoDict[key]=val
			with open(fpath,'a',encoding='utf8')as f:
				f.write(str(infoDict)+'\n')
				count=count+1
				print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
		except:
		    count=count+1
		    print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
		    continue

		
>>> def main():
	stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
	stock_info_url = 'https://gupiao.baidu.com/stock/'
	output_file = 'D:\BaiduStockInfo.txt'
	slist = []
	getStockList(slist, stock_list_url)
	getStockInfo(slist, stock_info_url, output_file)

	
>>> main()
>>> def getStockInfo(lst,stockURL,fpath):
	count=0
	for stock in lst:
		url=stockURL+stock+".html"
		html = getHTMLText(url)
		try:
			if html=="":
				continue
			infoDict = {}
			soup=BeautifulSoup(html,'html.parser')
			stockInfo=soup.find('div',attrs={'class':'stocks-bets'})
			infoDict.update({'股票名称':name.text.split()[0]})
			keyList=stockInfo.find_all('dt')
			valueList=stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key=keyList[i].text
				val=valueList[i].text
				infoDict[key]=val
			with open(fpath,'a',encoding='utf8')as f:
				f.write(str(infoDict)+'\n')
				count=count+1
				print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
		except:
		    count=count+1
		    print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
		    continue

>>> 
>>> main()
>>> def getHTMLText(url):
	try:
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		return r.text
	except:
		print("")

		
>>> main()
>>> def main():
	stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
	stock_info_url = 'https://gupiao.baidu.com/stock/'
	output_file = 'D://BaiduStockInfo.txt'
	slist = []
	getStockList(slist, stock_list_url)
	getStockInfo(slist, stock_info_url, output_file)

	
>>> def getStockList(lst,stockURL):
	html=getHTMLText(stockURL)
	soup=BeautifulSoup(html,'html.parser')
	a=soup.find_all('a')
	for i in a:
		try:
			href=i.attrs['href']
			lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
		except:
			continue

		
>>> def getHTMLText(url,code='utf8'):
	try:
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		r.encoding=code
		return r.text
	except:
		print("")

		
>>> main()

speed:0.02%
speed:0.04%
speed:0.06%
speed:0.09%
speed:0.11%
speed:0.13%
speed:0.15%
speed:0.17%
speed:0.19%
speed:0.21%
speed:0.23%
speed:0.26%
speed:0.28%
speed:0.30%




