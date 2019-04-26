#coding=utf-8

from src.utility.preprocess import handle_dataset
import pandas as pd
import sys
sys.path.append('..')

def complete_data():
    """
    本方法将之前处理好的数据集metadata_clean.csv加上导演、演员等剧组信息，同时加上关键字信息。之后返回
    """
    handle_dataset()
    clean_data = pd.read_csv('../movies_dataset/metadata_clean.csv')
    # 读取电影的制作人员信息
    cred = pd.read_csv('../movies_dataset/credits.csv')
    # 读取电影的关键字
    key = pd.read_csv('../movies_dataset/keywords.csv')

    # 确保'id'字段为整形
    clean_data = clean_data[clean_data.notnull()]
    cred['id'] = cred['id'].astype('int')
    key['id'] = key['id'].astype('int')

    # 合并
    clean_data = clean_data.merge(cred, on='id')
    clean_data = clean_data.merge(key, on='id')

    return clean_data