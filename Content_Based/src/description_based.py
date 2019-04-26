#coding=utf-8
"""
author: shayue
data: 2019/4/4
"""

from src.utility.add_overview import complete_data
import src.utility.TFIDF as TFIDF
from sklearn.metrics.pairwise import linear_kernel
from src.utility.content_recommender import content_recommender

if __name__ == '__main__':
    data = complete_data()
    tfidf_mat = TFIDF.tfidf(data['overview'])
    # cosine_sim[i][j] 代表movie_i 与movie_j根据内容计算的相似度，这是个对称矩阵，且主对角线始终为1
    cosine_sim = linear_kernel(tfidf_mat, tfidf_mat)

    movie = 'The Lion King'
    k = 5

    print("----------------这是基于电影描述内容的推荐----------------\n")
    print('如果您爱看电影%s，那么以下%d部电影也可能符合您的口味:\n' % (movie, k))
    print(content_recommender(movie, cosine_sim, data, k))
