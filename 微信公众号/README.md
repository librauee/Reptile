# 微信公众号文章
## [Link](https://mp.weixin.qq.com/s/Fqp9h27uwycbs_PJ3Tqggw)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/微信公众号/web.png)
## Target 
* 获取某微信公众号的全部内容，文章URL存入数据库，并以PDF的形式下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/微信公众号/download2.png)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/微信公众号/download1.png)
## Tips
* 常见方法一：通过搜狗微信去获取，但是只能获取最新的十篇文章
* 常见方法二：通过微信公众号的素材管理，获取公众号文章。但是需要有一个自己的公众号
* 通过Fiddler抓包发现链接的一些必要参数，在访问链接的时候带上这些参数，参数从抓包工具中获取
* 通过pdfkit这个模块导出pdf文件
* 上述模块需要安装[Wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)才能使用

## TODO
* 有比较大的局限性，每爬取一个公众号的所有文章，就需要通过抓包更新这些必要的参数

