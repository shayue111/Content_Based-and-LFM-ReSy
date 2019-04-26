#coding=utf-8
"""
author: shayue
data: 2019/4/1
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append('..')

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

def delete_exist_metadata_clean():
    if os.path.exists('../movies_dataset/metadata_clean.csv'):
        os.remove('../movies_dataset/metadata_clean.csv')
        print('正在处理数据集，请稍等！')


def handle_dataset():
    delete_exist_metadata_clean() # 若已经存在，则删除一遍，重新生成
    data = pd.read_csv('../movies_dataset/movies_metadata.csv', low_memory=False)

    # 测试
    # print(data.head())

    """1. 我们仅需要取其中的某些字段即可，即标题，电影类别，发行时间，时长，平均得分，打分人数，内容描述"""
    data = data[['title', 'genres', 'release_date', 'runtime', 'vote_average', 'vote_count', 'id']]

    """2. 处理电影类别字段'genres'，注意到它之前是一个字符串包含着一个列表，但是列表元素是字典，键是对应的类别id，在这里只想保留类别值"""
    data['genres'] = data['genres'].fillna('[]')  # 先对nan填充

    #  将字符串转成列表
    data['genres'] = data['genres'].apply(eval)

    # 最后仅保留类别，去掉类别id
    data['genres'] = data['genres'].apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])

    data['id'] = data['id'].apply(convert_int)
    # 测试
    # print(data.head())

    """3. 保存清理完的数据"""
    data.to_csv('../movies_dataset/metadata_clean.csv', index=False)
    print("已保存处理好的数据集到movies_dataset/metadata_clean.csv")
    print('-------------------------------------------------------')
# if __name__ == '__main__':
#     handle_dataset()