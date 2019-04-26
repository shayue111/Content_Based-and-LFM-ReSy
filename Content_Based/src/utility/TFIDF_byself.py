from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
import numpy as np
import pandas as pd

# 语料库
corpus = [
    'this is the first document',
    'this is the second document',
    'and the third one.',
    'Is this the first document?',
    'I come to American to travel'
]

"""
[[0 0 0 1 1 1 0 0 1 0 1 0 0]
 [0 0 0 1 0 1 0 1 1 0 1 0 0]
 [0 1 0 0 0 0 1 0 1 1 0 0 0]
 [0 0 0 1 1 1 0 0 1 0 1 0 0]
 [1 0 1 0 0 0 0 0 0 0 0 2 1]]
[[0.         0.         0.         0.4402705  0.53038867 0.4402705
  0.         0.         0.37036943 0.         0.4402705  0.
  0.        ]
 [0.         0.         0.         0.41039975 0.         0.41039975
  0.         0.61280066 0.3452412  0.         0.41039975 0.
  0.        ]
 [0.         0.54903633 0.         0.         0.         0.
  0.54903633 0.         0.30931749 0.54903633 0.         0.
  0.        ]
 [0.         0.         0.         0.4402705  0.53038867 0.4402705
  0.         0.         0.37036943 0.         0.4402705  0.
  0.        ]
 [0.37796447 0.         0.37796447 0.         0.         0.
  0.         0.         0.         0.         0.         0.75592895
  0.37796447]]
"""

# 获取英文停位词



class tfidf(object):
    """手动实现tfidf。输入的corpus是个ndarray数组"""

    def __init__(self, corpus):
        self.matrix = None           # 语料库经hand_corpurs方法处理后将单词存在matrix中
        self.split_words = []       # corpus传入后，对corpus中的每个句子作一些修改，然后将每个句子分词后存入split_words。split_words是个二维列表
        self.all_words = {}         # all_words是个字典，键是corpus中所有出现的单词（除了停位词），值是键的下标
        self.symbol = ['.', '?']    # 可能出现在句子末尾的标点符号
        self.stop_words = get_stop_words('en')     # 停位词
        self.hand_corpurs(corpus)   # 处理遇到人名、地名等情况
        self.map_matrix()

    def hand_corpurs(self, corpus):
        allwords = []
        for sentence in corpus:
            tmp_words = []
            # 处理句子的最后一个单词，因为它可能带有标点符号
            words = sentence.split(sep=' ')
            # print("处理前",words[-1])
            if words[-1][-1] in self.symbol:  # 如果句子的最后一个单词有标点符号，将它去掉
                words[-1] = words[-1][:-1]
            for word in words:
                word = word.lower()
                if word in self.stop_words:  # 如果单词属于停用词，则不考虑它
                    continue
                if word not in allwords:
                    allwords.append(word)
                tmp_words.append(word)

            self.split_words.append(tmp_words)

        allwords.sort()
        for i, word in enumerate(allwords):
            self.all_words[word] = i

    def map_matrix(self):
        self.matrix = np.zeros(shape=(len(self.split_words), len(self.all_words)), dtype=np.int)
        row = 0
        for words in self.split_words:
            for word in words:
                if word in self.all_words.keys():
                    self.matrix[row][self.all_words[word]] += 1
            row += 1

    def get_feature_names(self):
        return self.all_words.keys()


if __name__ == '__main__':
    vectorizer = CountVectorizer()
    words = vectorizer.fit_transform(corpus)

    tf_idf = TfidfTransformer().fit_transform(words)

    obj = tfidf(corpus)
    columns = obj.get_feature_names()
    data = pd.DataFrame(data=obj.matrix, columns=columns)
    # print(data)
    # 接下来就是整合频率，和每个单词在文档中出现的次数。参考https://blog.csdn.net/u012421852/article/details/79575740
    n = (obj.matrix.shape[0])
    Fre = (obj.matrix.sum(axis=0))
    lig = np.log((1+n)/(1+Fre)) + 1

    lig = obj.matrix * lig
    # print(lig)
    for i in range(5):
        arr = lig[i]
        f = np.sqrt(np.sum(arr ** 2))
        lig[i] = arr / f
    # print(lig)
    # print('------')
    # print(tf_idf.toarray())


