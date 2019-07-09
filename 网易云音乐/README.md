# 网易云音乐评论
## [Link](https://music.163.com/#/song?id=1374051000)
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/网易云音乐/web.png)
## Target 
* 获取薛之谦的新歌木偶人评论信息，并下载到本地存储
![在这里插入图片描述](https://github.com/librauee/Reptile/blob/master/网易云音乐/download.png)
## Tips
*  存入csv文件中，需要将 encoding改为'utf-8_sig'，不然会出现乱码
*  UTF-8以字节为编码单元，它的字节顺序在所有系统中都是相同的，没有字节序的问题，也因此它实际上并不需要BOM(“ByteOrder Mark”), 但是UTF-8 with BOM即utf-8-sig需要提供BOM（"ByteOrder Mark"）
* 一种无需提供post参数的apk：http://music.163.com/api/v1/resource/comments/R_SO_4_1374051000，直接加上offset作为偏移量即可

