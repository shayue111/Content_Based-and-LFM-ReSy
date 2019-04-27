"""
数据集已经整理为如下形式后，利用read_item_info对item的内容作更详细的提取
['1', 'Toy Story (1995)', '01-Jan-1995', '', 'http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0\n']

返回的一个字典有：
id  - int
title - str
time - str
detail - str
genre - dict，
如
{
    '1':{'title':'Toy Story (1995)', 'year':'01-Jan-1995', 'detail':'http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)', 'genre': }
}
"""
import sys
sys.path.append('..')


def get_genres(path='../MovieLens/u.genre'):
    """
    读取u.genre中的信息，返回一个字典。字典包含类别id以及电影对应的类别
    """
    # 待返回的字典
    genre_dict = {}
    with open(path) as files:
        for line in files:
            # 读取每一行，去掉最后的换行符并以'|'分割
            tmp_list = line.rstrip('\n').split(sep='|')
            # 加入字典
            genre_dict[int(tmp_list[1])] = tmp_list[0]

    return genre_dict


def read_item_info(path='../MovieLens/u.item'):
    """
    希望最终处理得到的信息如下所示
    ['1', 'Toy Story', '01-Jan-1995', 'http://us.imdb.com/M/title-exact?Toy%20Story%20',['Animation', "Children's", 'Comedy']]
    """
    # 获取类别字典
    genres_dict = get_genres()
    with open(path) as lines:
        for line in lines:
            # 获取每一行的信息，去掉回车，以'|'切割
            tmp_list = line.rstrip('\n').split(sep='|', maxsplit=5)
            tmp_list.remove('')
            # 由于已经有时间的信息字段，因此将标题与地址页中的年份信息去掉
            id = tmp_list[0]
            title = tmp_list[1][:-7]
            time = tmp_list[2]
            address = tmp_list[3][:-6]
            genres_bin = tmp_list[4].split('|')
            the_genres = []
            for i in range(len(genres_bin)):
                if genres_bin[i] == '1':
                    the_genres.append(genres_dict[i])

            print(id, title, time, address, the_genres)
            # 将信息整合到一个新字典中


if __name__ == '__main__':
    print(read_item_info())
