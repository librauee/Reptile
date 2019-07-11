# 豆瓣电影Top250

## 开发环境
* 安装Python环境，推荐Anaconda，能减少很多库安装的问题
* 安装Scrapy
 [官方文档](https://doc.scrapy.org/en/latest/intro/install.html)提供了详细的安装方法
* 安装MongoDB
  使用MongoDB来保存爬取到的网页上的信息，如文章的标题、类别、图片保存路径等等。
## 爬取实战
### 工程创建
打开命令行，开启第一个Scrapy项目的实践
```
scrapy startproject douban
```
项目创建完成后可以看到在工程创建的位置有了douban文件夹，打开以后包含了上述的组件，可以使用spyder,pycharm等ide打开项目![在这里插入图片描述](https://img-blog.csdnimg.cn/20190710095046677.png)
根据命令行的提示
```
cd douban
scrapy genspider example example.com
```
进入douban文件夹，并创建spider,上述命令中的example替换为spider的名字doubanmovie，example.com替换为 douban.com ,输入上述命令之后可以看到多了一个spider的py文件。
### 代码编写
#### Settings
* 需要设置USER_AGENT,假装自己是浏览器访问网页。下面给多个用户代理，随机选择其中之一进行访问，在settings.py中加入以下代码
   ```py
   user_agent_list = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    USER_AGENT = random.choice(user_agent_list)
    ```
 * 编写完pipeline类之后需要继续在settings py中进行配置, 可以配置多个pipeline, 300为优先级, 值越低, 优先级越高, 范围在(0, 1000)内。
    ```py
    ITEM_PIPELINES = {
   'douban.pipelines.DoubanPipeline': 300,}
    ```
#### Items
* 在items.py中编写一个item用于存放爬取结果
```py
import scrapy

class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影标题
    title = scrapy.Field()
    # 豆瓣评分
    star = scrapy.Field()
    # 主演信息
    Staring = scrapy.Field()
    # 豆瓣排名
    rank = scrapy.Field()
    # 描述
    quote = scrapy.Field()
    # 豆瓣详情页
    url = scrapy.Field()
```

#### Doubanmovie
* 这里是爬虫的部分，在spiders目录下doubanmovie.py文件中进行编辑，爬虫的逻辑非常简单，这里选择了官方文档推荐的css方法来解析html。[Scrapy的CSS选择器](http://www.scrapyd.cn/doc/185.html)
* 通过对网页源代码的分析, 我们发现我们所要获取的信息都在class为item中的div中, 遍历这些div, 获取相关数据.每一页有有25部电影数据, 当这一页的数据获取完成后, 接着爬取下一页的数据，下一页的链接藏在标签里，同样通过css选择器提取。当然也可以通过xpath，BeautifulSoup来解析网页。
```py
import scrapy
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    start_urls = ['https://movie.douban.com/top250']
    def parse(self, response):
        for item in response.css('.item'):
            movie = DoubanItem()
            #Staring = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()').extract_first()
            Staring =item.css('.bd p::text').extract_first()
            rank = item.css('.pic em::text').extract_first()
            title = item.css('.hd span.title::text').extract_first()
            star = item.css('.star span.rating_num::text').extract_first()
            quote = item.css('.quote span.inq::text').extract_first()
            url = item.css('.pic a::attr("href")').extract_first()
            image_url = item.css('.pic img::attr("src")').extract_first()
            movie['rank'] = rank
            movie['title'] = title
            movie['star'] = star
            movie['Staring'] = Staring
            movie['quote'] = quote
            movie['url'] = url
            movie['image_url'] = image_url
            yield movie
    
        # 获取下一页的url
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)
```

#### Pipelines
* 这里将数据存入MongoDB数据库
```py 
class DoubanPipeline(object):

    def __init__(self) -> None:
        # 连接
        self.client = MongoClient(host='localhost', port=27017)
        # 如果设置有权限, 则需要先登录
        # db_auth = self.client.admin
        # db_auth.authenticate('root', 'root')
        # 需要保存到的collection
        self.col = self.client['douban_movie']
        self.top250 = self.col.top250
        # 先清除之前保存的数据
        # self.top250.delete_many({})

    def process_item(self, item, spider):
        res = dict(item)
        self.top250.insert_one(res)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()
```

#### 爬虫运行
* 进入项目所在文件夹，在命令行输入如下指令
```
scrapy crawl doubanmovie
```
* 也可以选择下面的命令，同时输出json文件
```
scrapy crawl doubanmovie -o top250.json -s FEED_EXPORT_ENCODING=UTF-8
```

### 爬取成果
* json文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190710103917933.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x5YzQ0ODEzNDE4,size_16,color_FFFFFF,t_70)
* MongoDB数据库
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190710104012262.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x5YzQ0ODEzNDE4,size_16,color_FFFFFF,t_70)
