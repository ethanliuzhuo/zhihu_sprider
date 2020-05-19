# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:45:39 2020

@author: ethan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:37:45 2020

@author: ethan
"""


# coding: utf-8
# 2020/03 by florakl

from util import url_get
import json
from datetime import datetime
from util import url_get
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
import os

def question_info_get(qid): 
    """
    获取回答数量，问题和创造时间

    Parameters
    ----------
    qid : int
        question id.

    Returns
    -------
    total ：int
        该问题回答数量
    title： str
        问题标题
    created_time: time
        问题提问时间

    """
    q_url = f'https://www.zhihu.com/api/v4/questions/{qid}?include=answer_count'
#    print(q_url)
    q_res = url_get(q_url)
    if q_res:
        total = q_res['answer_count']  # 回答数
        title = q_res['title']  # 问题标题
        created_time = q_res['created']  # 创建时间
        return total, title, created_time


def answer_time_get(qid, interval, offset, q_time):
    """
    获取单个回答下的一组回答

    Parameters
    ----------
    qid : int
        question id.
    interval : int
        起始位置.
    offset : int
        间隔数，每间隔这个数爬取一次回答内容.
    q_time : time
        追加时间.

    Returns
    -------
    content,name,gender,voteup_count,comment_count,ad_answer
    内容 回答者姓名 回答者性别 点赞数 赞同数 是否追打 、
    全部为list格式

    """

    content = []
    name = []
    gender = []
    voteup_count = [] #赞同
    comment_count = [] #评论
    ad_answer = []
    
    ans_url = f'https://www.zhihu.com/api/v4/questions/{qid}/answers?include=content,comment_count,voteup_count&limit={interval}&offset={offset}&sort_by=default'
    ans_res = url_get(ans_url)
#    print(ans_url)
    answers = ans_res['data']
    for answer in answers:
        content.append(answer['content'])
        name.append(answer['author']['name'])
        gender.append(answer['author']['gender'])
        voteup_count.append(answer['voteup_count'])
        comment_count.append(answer['comment_count'])
        ad_answer.append(answer['ad_answer'])
        # ans_time.append(answer['created_time'] - q_time)
    return content,name,gender,voteup_count,comment_count,ad_answer


def data_get(qid, number):
    """
    爬取问题下的数据，包括回答，点赞数，回答者，性别，点赞数，留言数，是否追答

    Parameters
    ----------
    qid : int
        question id.
    number : int
        显示第几个问题.

    Returns
    -------
    answers : list
        加入list.
    total : int
        该问题有多少个回答.

    """
    total, title, created_time = question_info_get(qid)
    interval = 20
    offset = 0
    contents = []
    names = []
    genders = []
    voteup_counts = []
    comment_counts = []
    ad_answers = []
    
    answers = [str('title: ' + title)] #加入问题
    localtime = time.asctime( time.localtime(time.time())) #显示时间
    if total < 5: #如果该问题数小于 5 个，那么将跳过该问题
        print(f'{localtime} 第{number}个问题回答数小于5，qid={qid}跳过')
        return None
    else:
        while offset < total:
            if offset%3000 == 0: #每3000次显示一次，比显示占比
                percent = offset/total
                
                # print(f'{localtime} 正在爬取第{number}问题',f'qid= {qid} total = {total}','占比 = ' + '{:.0%}'.format(percent))
            try:
                content,name,gender,voteup_count,comment_count,ad_answer = answer_time_get(qid, interval, offset, created_time)
                names += name
                contents += content
                genders += gender
                voteup_counts += voteup_count
                comment_counts += comment_count
                ad_answers += ad_answer
                
            except:
                print(f'{localtime} 正在爬取第{number}问题,qid= {qid}失败')
                continue
            # 单次爬取回答个数上限为20
            # names += name
            # contents += content
            # genders += gender
            # voteup_counts += voteup_count
            # comment_counts += comment_count
            # ad_answers += ad_answer
            
            offset += interval
        # print(f'第{number}个问题爬取成功，id={qid}，标题=“{title}”，总回答数={total}')
        for i in range(len(contents)):
            try: #每一个问题保存为字典格式
                answer = {}
                answer['qid'] = qid #问题编号
                answer['contents'] = contents[i] #回答内容
                answer['names'] = names[i] #回答者昵称
                answer['genders'] = genders[i] #回答者性别
                answer['voteup_counts'] = voteup_counts[i] #点赞数
                answer['comment_counts'] = comment_counts[i] #留言数量
                answer['ad_answers'] = ad_answers[i] #是否追答
            except:
                continue
            answers += [answer]
            
        
        return answers,total
    
def save_answer(qid,number):
    """
    保存该问题下的所有答案，保存为json文件

    Parameters
    ----------
    qid : int
        question id.
    number : int
        显示第几个问题.

    Returns
    -------
    None.

    """
    data,total = data_get(qid, number)
    if data:
        filename = f'data/data{qid}.json'
        with open(filename, 'w') as f:
            json.dump(data, fp=f, indent=4)
        print(f'第{number}个问题爬取成功，id={qid}，总回答数={total}')
    
    
def start_thread(count):
    """
    启动线程池执行下载任务

    Parameters
    ----------
    count : int
        线程池数量.

    Returns
    -------
    None.

    """
    # qids = [314644210, 30265988, 26933347, 33220674, 264958421, 31524027]
    qids = pd.read_csv('qid_csv.csv',encoding ='utf-8')
    qids = qids['qid']
    qids = list(set(qids)) #只保留唯一的qid
    # qids = [314644210]
    number = 1
    pids_got= os.listdir('D:\\Project\\爬虫\\zhihu\\data') 
    pids_got = [i[4:-5] for i in pids_got]
    
    pids_got = list(map(int, pids_got))
    qids = list(set(qids) - set(pids_got)) #list相减，只保留未背爬取的qid
    
    with ThreadPoolExecutor(max_workers=count) as t: 
        for qid in qids[:]:
            if str(qid) not in pids_got:
                t.submit(save_answer, qid,number)
                number += 1
            else:
                print(f'该{qid}已经有了')
                number += 1
                continue
            
            
if __name__ == "__main__":
    print("程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束")
         
            
# if __name__ == '__main__':
#     # qids = [314644210, 30265988, 26933347, 33220674, 264958421, 31524027]
#     qids = pd.read_csv('qid_csv.csv',encoding ='utf-8')
#     qids = qids['qid']
#     qids = list(set(qids))
#     # qids = [314644210]
#     number = 2020
    
#     for qid in qids[number:]:
#         data = data_get(qid, number)

#         number += 1
#         if data:
#             filename = f'data{qid}.json'
                    
#             with open(filename, 'w') as f:
#                 json.dump(data, fp=f, indent=4)
#                 print(f'{qid}数据保存成功')