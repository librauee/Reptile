# 拉钩职位信息
## [Link](https://www.lagou.com/)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/拉钩/web.png)
## Target 
* 获取Python相关的职位信息，并下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/拉钩/download.png)
## Tips
* headers中需写入**Referer**，不然会报错，在同一次session中访问，提取cookies
```python
'status': False, 'msg': '您操作太频繁,请稍后再访问', 'clientIp': '117.136.41.41', 'state': 2402
```
* 在请求中去掉timeout，不然容易提取未加载的新页面
```
<script type="text/javascript">gRltTszy();</script>页面加载中...<script type="text/javascript" src="https://www.lagou.com/upload/oss.js"></script>
```
* 调用csv模块，可以将数据写入csv文件
```python
import csv
with open('lagou_data.csv','w',encoding='gbk',newline='') as f:
    csv_write = csv.writer(f)
    title = ['id','职位','城市','学历','工作年限','薪资','第一标签','第二标签','第三标签','技能库','公司名称','融资阶段','公司规模']
    csv_write.writerow(title)
```

## TODO
* 依然会出现 “页面加载中”的情况，难以获得所有的具体招聘要求和职位描述
 
