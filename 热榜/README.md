# 知乎、微博热榜

## Target 
* 爬取知乎微博热榜并定时更新


![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/热榜/hot.png)

## Tips

* apscheduler 的应用 ,间隔20分钟运行

```python
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler=BlockingScheduler()
scheduler.add_job(func=main,trigger='interval',minutes=20)
scheduler.start()
```
* 具体详解请查看公众号推文~



