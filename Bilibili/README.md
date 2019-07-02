# 哔哩哔哩小视频
## [Link](http://vc.bilibili.com/p/eden/rank#/?tab=%E5%85%A8%E9%83%A8)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/Bilibili/top.png)
## Target 
* 获取所有排行榜上的小视频，下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/Bilibili/vedio.png)
## Tips
* 获取来自服务器的原始套接字响应,需要在初始请求中设置 stream=True
* 当流下载时，用Response.iter_content或许更方便些。requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content 来边下载边存硬盘
* tqdm进度条 
'''
for data in tqdm(iterable):
    pass
'''
## Todo
* 视频文件名无法正确存储，这里用数字代替
