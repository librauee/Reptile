# 今日头条街拍图片
## [Link](https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/今日头条/web.png)
## Target 
* 获取街拍图片，并下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/今日头条/download.png)
## Tips
* urlencode用来拼接url链接
* 利用了多线程或者多进程来处理
* 图片的名称使用其内容的MD5值，这样可以去除重复
* 构造一个生成器，将图片链接和图片所属的标题一并返回
```python
for image in images:
    yield {
             'image': image.get('url'),
             'title': title
                }
```
* 利用正则表达式将不符合命名规范的title去除

