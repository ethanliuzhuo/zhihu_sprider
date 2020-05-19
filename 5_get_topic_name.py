# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:26:31 2020

@author: ethan
"""

from util import url_get
import json
from datetime import datetime
from util import url_get
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
import os
import requests
from bs4 import BeautifulSoup

def question_info_get(qid):
    """
    获取问题的标签

    Parameters
    ----------
    qid : int
        question id.

    Returns
    -------
    keywords：list
        问题关键词

    """
    headers = {
    "User-Agent": "",
    "Connection": "",
    "Accept": "",
    "Accept-Language": ""}
    q_url = f'https://www.zhihu.com/question/{qid}'
    
#    print(q_url)
    try:
        html = requests.get(q_url, headers=headers, timeout=20)
        html.encoding ='utf-8'
        soup =BeautifulSoup(html.text,'lxml')
   
        keywords = str(soup.find('meta', {'name': 'keywords'}))
        keywords = keywords.split('"')[1].split(',')
        return keywords
    except:
        return []
    
def get_qid_list(path):
    """
    把文件目录下的所有文件名变为list

    Parameters
    ----------
    path : str
        问题所有路径.

    Returns
    -------
    list
        文件名.

    """
    return os.listdir(path)

def get_qid(qid_file_name):
    """
    提取该文件名的question id

    Parameters
    ----------
    qid_file_name : str
        文件名.

    Returns
    -------
    qid : int
        question id.

    """
    qid = int(qid_file_name.split('data')[1].split('.')[0])
    return qid

def save_answer(qid,keywords,path):
    """
    把获得到的关键词，添加进入原回答

    Parameters
    ----------
    qid : int
        question id.
    keywords : list
        关键词.
    path : str
        数据的储存文件路径.

    Returns
    -------
    None.

    """
    answer_path = path + '/data' + str(qid) + '.json'
    with open(answer_path, 'r') as f:
        answer_data = json.loads(f.read())
    answer_data.insert(1, keywords)

    with open(answer_path, 'w') as f:
        json.dump(answer_data, fp=f, indent=4)

def zheng_he(qid_file_name,path,index):
    """
    调用以上的所有函数，整合到一起

    Parameters
    ----------
    qid_file_name : str
        文件名.
    path : str
        数据的储存文件路径..
    index : int
        第几个问题.

    Returns
    -------
    None.

    """
    try:
        qid = get_qid(qid_file_name)
        keywords = question_info_get(qid)
        save_answer(qid,keywords,path)
        if index%1000 == 0: #每 1000 次进行输入
            percent = index/76589
            print(str(index),' 占比 = ' + '{:.4%}'.format(percent))
    except:
        print(str(qid) + ' error')
        pass

        # qid = get_qid(qid_file_name)
        # keywords = question_info_get(qid)
        # save_answer(qid,keywords,path)
        # if index%5 == 0:
        #     percent = index/55
        #     print(str(index),' 占比 = ' + '{:.0%}'.format(percent))
        

    
def start_thread(count):
    """
    启动线程池执行下载任务

    Parameters
    ----------
    count : int
        启用线程数.

    Returns
    -------
    None.

    """
    path = 'data'
    qid_list = get_qid_list(path)
    
    with ThreadPoolExecutor(max_workers=count) as t:
        for index, qid_file_name in enumerate(qid_list):
            t.submit(zheng_he, qid_file_name, path,index)


if __name__ == "__main__":
    print("程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束")
