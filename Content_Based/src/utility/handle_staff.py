import numpy as np

def take_away_str(data):
    """去掉对应字段的值外面的引号，比如'[1,2,3]'去掉变为列表[1,2,3]"""
    features = ['cast', 'keywords', 'genres', 'crew']
    for feature in features:
        data[feature] = data[feature].apply(eval)
    return data

def get_director(members):
    for crew_member in members:
        if crew_member['job'] == 'Director':
            return crew_member['name']
    return np.nan

def get_cast_keywords(stuffs):
    if isinstance(stuffs, list):
        names = [x['name'] for x in stuffs]
        # 为了简便，仅取前3位
        if len(names) > 3:
            names = names[:3]
        return names

    # 如果cast不是个列表，那么直接返回空列表了
    return []

def manipulate(data):
    data = take_away_str(data)
    # 创建导演字段
    data['director'] = data['crew'].apply(get_director)
    # 创建主演字段
    data['cast'] = data['cast'].apply(get_cast_keywords)
    # 创建关键字字段
    data['keywords'] = data['keywords'].apply(get_cast_keywords)

    # 取这些作为判断相似程度的内容组成新的数据返回
    data = data[['title', 'cast', 'keywords', 'genres', 'director']]

    return data
