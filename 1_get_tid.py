# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:05:01 2020

@author: ethan
"""

# coding: utf-8
# 2020/03 by florakl

import json
from datetime import datetime
from util import url_get
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

def tid_get(tid):
    """
    知乎根话题下的精华问题
    获取topic id，检查是否能用

    Parameters
    ----------
    tid : int
        topic id.

    Returns
    -------
    tid : int
        返回可用的topic id.

    """
    url = f'https://www.zhihu.com/api/v4/topics/{tid}'
    res = url_get(url)
    try:
        res['unanswered_count']
        print(tid)
        return tid
    except:
        pass

def tids_get(tid,tids,i):
    """
    添加可用的topic id 进入list

    Parameters
    ----------
    tid : int
        topic id.
    tids : list
        topic id list.
    i : int
        tid + i = new tid.

    Returns
    -------
    None.

    """
    try:
        tidz = tid_get(tid+i)
        tids += [tidz]
    except:
        pass

def start_thread(count):
    """
    启动线程池执行下载任务
    保存tid 为 csv文件，为后续做准备

    Parameters
    ----------
    count : int
        线程数数量.

    Returns
    -------
    None.

    """
    # number = 1
    tid = 19776751 + 400000
    tids = []
    with ThreadPoolExecutor(max_workers=count) as t:
        for i in range(1, 100000, 1):
            t.submit(tids_get, tid,tids,i)
    tids = list(filter(None, tids))
    tis_pd = pd.DataFrame(tids,columns = ['tid'])
    tis_pd.to_csv('tids.csv',encoding='utf-8',index=0)


    
if __name__ == '__main__':
    print("程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束")