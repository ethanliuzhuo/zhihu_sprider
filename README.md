# 知乎问题爬虫
知乎回答爬取下载（非文章）

顺序是

1.先获取可用topic id（1.py）
返回得到一个tid.csv

2.获取可用question id（2.py）
返回得到一个qid.csv

3.获取该问题的回答（4.py）
将答案储存到data文件夹里面

4.获取该问题的关键词（5.py）
将data文件夹的文件更新


## 要不断地更新ip，否则会失效
