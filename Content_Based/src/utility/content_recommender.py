#coding=utf-8
"""
author: shayue
data: 2019/4/12
"""
import pandas as pd

def content_recommender(title, similarity, data, k):
    # 获取电影在data中是第几行
    indices = pd.Series(data.index, index=data['title']).drop_duplicates()
    idx = indices[title]

    # 通过enumerate可以为等下获取下标提供方便
    sim_scores = list(enumerate(similarity[idx]))

    # 按照相似程度从大到小排序
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 忽略第一排名最高，因为就是其本身。取k部最相似的电影返回
    sim_scores = sim_scores[1:k+1]

    # 获取最相似的k部电影的下标
    movie_indices = [i[0] for i in sim_scores]

    # 返回一个列表
    return list(data['title'].iloc[movie_indices].values)