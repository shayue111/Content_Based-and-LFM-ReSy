import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('..')

def get_rating_matrix(path):
    rating_matrix = {}
    user_size = 0
    item_size = 0
    with open(path) as files:
        for line in files:
            split_list = line.rstrip('\n').split('\t')
            user_id, item_id, rating = int(split_list[0]), int(split_list[1]), float(split_list[2])

            if user_id > user_size:
                user_size = user_id

            if item_id > item_size:
                item_size = item_id

            if user_id not in rating_matrix.keys():
                rating_matrix.setdefault(user_id, {})
            rating_matrix[user_id][item_id] = rating
    return rating_matrix, user_size, item_size

def SGD(rating_matrix, user_size, item_size, latent, lr, Lambda, epochs):
    # 初始化
    residual_rec = []

    user_vector = np.random.randn(user_size, latent)
    item_vector = np.random.randn(item_size, latent)

    # 迭代epochs轮
    for epoch in range(epochs):
        # 遍历全部矩阵更新
        sum = 0
        iters = 0
        for i in rating_matrix.keys():
            for j in rating_matrix[i].keys():
                residual = rating_matrix[i][j] - np.dot(user_vector[i-1], item_vector[j-1])
                sum += abs(residual)
                iters += 1
                user_vector[i-1] += lr * (residual * item_vector[j-1] - Lambda * user_vector[i-1])
                item_vector[j-1] += lr * (residual * user_vector[i-1] - Lambda * item_vector[j-1])
                # print(user_vector[i-1],'\n', item_vector[j-1])
        # print("在epoch%d，平均的residual是%f" % ((epoch+1), round(sum/iters, 3)))
        residual_rec.append(round(sum/iters, 3))
    # plt.plot(range(epochs), residual_rec)
    # plt.show()

    return user_vector, item_vector

if __name__ == '__main__':
    rating_matrix, user_size, item_size = get_rating_matrix('../MovieLens/ua.base')
    user_vector, item_vector = SGD(rating_matrix, user_size, item_size, 50, 0.003, 0.5, 25)

    # 之后来做预测
    test_matrix, _, _ = get_rating_matrix('../MovieLens/ua.test')

    rating_rec = []
    rating_hat_rec = []
    total_loss = 0
    time = 0
    for i in test_matrix.keys():
        for j in test_matrix[i].keys():
            rating = test_matrix[i][j]
            rating_hat = np.dot(user_vector[i-1], item_vector[j-1])
            # rating_rec.append(rating)
            # rating_hat_rec.append(rating_hat)
            loss = (rating - rating_hat) ** 2
            total_loss += loss
            time += 1

    print("SSE", total_loss/time)
    # plt.scatter(range(len(rating_rec)), rating_rec, s=1.0)
    # plt.scatter(range(len(rating_hat_rec)), rating_hat_rec, s=1.0)
    # plt.legend()
    # plt.show()
