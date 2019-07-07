# 拉钩职位信息
## [Link](https://www.lagou.com/)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/拉钩/web.png)
## Target 
* 获取Python相关的职位信息，并下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/拉钩/download.png)
## Tips
* headers中需写入**Referer**，不然会报错
* 调用csv模块，可以将数据写入csv文件
```python
import csv
with open('lagou_data.csv','w',encoding='gbk',newline='') as f:
    csv_write = csv.writer(f)
    title = ['id','职位','城市','学历','工作年限','薪资','第一标签','第二标签','第三标签','技能库','公司名称','融资阶段','公司规模']
    csv_write.writerow(title)
```
