# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:47:50 2020

@author: ethan
"""

# coding: utf-8
# 2020/03 by florakl

import json
from datetime import datetime
from util import url_get
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def qid_get(tid, interval, offset):
    """
    知乎根话题下的精华问题
    获取单个话题下的所有问题，即question id（qid）

    Parameters
    ----------
    tid : int
        单个topic id.
    interval : int
        起始位置.
    offset : int
        每间隔多少个爬取一次.

    Returns
    -------
    qids : list
        获取到的所有question id.

    """
    # 知乎根话题下的精华问题
    # tid = 19776751
    url = f'https://www.zhihu.com/api/v4/topics/{tid}/feeds/essence?limit={interval}&offset={offset}'
    # print(url)
    res = url_get(url)
    qids = []
    # print(2)
    # print(res)
    if res:
        for question in res['data']:
            try:
                qid = question['target']['question']['id']
                # print('pid begin:',qid)
                qids.append(qid)
            except KeyError:
                print('qid无法读取，跳过该问题')
    else:
        print(tid + 'qid_get error')
    return qids


# def qids_get(tid,qid_csv,error = 0):
#     # 单次爬取问题个数上限为10
#     for i in range(0, 1000, 10):
#         # 单次爬取问题个数上限为10
        
#         try:
#             qids = qid_get(tid,interval=10, offset=i)
#             print('qids',qids)
#         except:
#             print('time error')
#             continue
#         if error == 5:
#             break
        
#         if len(qids) != 0:
#             print(i,'succuss')
#             df = pd.DataFrame(qids,columns = ['qid'])
#             qid_csv = qid_csv.append(df, ignore_index=True)
#             qid_csv.to_csv('qid.csv',encoding='utf-8',index=0)
#         else:
#             print('error')
#             error += 1
#             continue


# def start_thread(count):
#     """
#     启动线程池执行下载任务
#     :return:
#     """
#     # number = 1
#     tid_csv = pd.read_csv('tids_csv.csv',encoding ='utf-8')
#     tids = tid_csv['tid']
#     qid_csv = pd.read_csv('qid.csv',encoding ='utf-8')
    
#     with ThreadPoolExecutor(max_workers=count) as t:
#         for tid in tids[7736:]:
#             print('tid:',tid)
#             error = 0
#             t.submit(qids_get, tid,qid_csv,error)

    
# if __name__ == '__main__':
#     print("程序执行开始")
#     print("======================================")
#     print("温馨提示： 输入内容必须为大于的0的数字才行！")
#     print("======================================")
#     count = int(input("请输入您需要启动的线程数： "))
#     start_thread(count)
#     print("程序执行结束")


if __name__ == '__main__':
    """
    单线程
    """
    number = 1
    tid_csv = pd.read_csv('tids_csv.csv',encoding ='utf-8')
    tids = tid_csv['tid']
    qid_csv = pd.read_csv('qid_csv.csv',encoding ='utf-8')
    
    for tid in tids[22875:]: #tid 起始位置，过去的不用爬了
        print('tid:',tid)
        error = 0
        for i in range(0, 1000, 10):
            # 单次爬取问题个数上限为10
            
            try:
                qids = qid_get(tid,interval=10, offset=i)
                # print('qids',qids)
            except:
                print('time error')
                continue
            if error == 5: #如果出现5次error，则跳过
                break
            
            if len(qids) != 0: #检查qids 是否为空
                print(i,'succuss')
                df = pd.DataFrame(qids,columns = ['qid'])
                qid_csv = qid_csv.append(df, ignore_index=True)
                qid_csv.to_csv('qid_csv.csv',encoding='utf-8',index=0)
            else:
                print('error')
                error += 1
                continue