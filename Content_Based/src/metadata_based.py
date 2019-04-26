#coding=utf-8
"""
author: shayue
data: 2019/4/8
"""

from src.utility.add_staff_keyword import complete_data
from src.utility.handle_staff import manipulate
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utility.content_recommender import content_recommender

def unify(x):
    if isinstance(x, list):
        # 去掉空格
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # director字段为str，如果不为str，返回空字符串
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def create_soup(x):
    soup = ''
    for feature in ['cast', 'keywords', 'genres', 'director']:
        if feature == 'director':
            soup += x[feature]
        else:
            for i in x[feature]:
                soup += i
                soup += ' '
    return soup

if __name__ == '__main__':
    data = complete_data()
    data = manipulate(data)

    # 为了避免二义性，需要将人名、类别名等都变为小写，并且去掉空格，再将这些字段合并到一起成为一个新的字段
    for feature in ['cast', 'keywords', 'genres', 'director']:
        data[feature] = data[feature].apply(unify)

    # 创建新字段soup将这些metadata融合在一起
    data['soup'] = data.apply(create_soup, axis=1)

    # 将soup中的metadata转化为词向量
    count = CountVectorizer(stop_words='english')
    count_mat = count.fit_transform(data['soup'])
    cosine_sim = cosine_similarity(count_mat, count_mat)

    movie = 'The Lion King'
    k = 5

    print("----------------这是基于电影元数据的推荐----------------\n")
    print('如果您爱看电影%s，那么以下%d部电影也可能符合您的口味:\n' % (movie, k))
    print(content_recommender(movie, cosine_sim, data, k))


