# -*- coding: utf-8 -*-

import numpy as np


# 正态分布的朴素贝叶斯分类器
class NaiveBayesContinuous:

    def __init__(self):
        self.mean = []
        self.std = []
        self.label_array = []
        self.prediction = []
        self.test_data = []

    # 保存模型
    def save_model(self):
        path = 'model.npz'
        np.savez(path, self.mean, self.std, self.label_array)
        print('save complete')

    # 加载模型
    def load_model(self):
        path = 'model.npz'
        model = np.load(path)
        self.mean = model['arr_0']
        self.std = model['arr_1']
        self.label_array = model['arr_2']

    # 训练模型
    def train_model(self, train_data):
        self.mean, self.std, self.label_array = self.get_mean_std_label(train_data)

    # 获取训练集每个特征的均值和方差以及类标签的取值集合
    @staticmethod
    def get_mean_std_label(train_data):
        label_counts = train_data.label.value_counts()
        label_arr = np.array(label_counts.index)
        label_arr.sort()
        # 得到除标签外特征数
        num_feature = len(train_data.columns.values) - 1
        # 按类别划分数据
        names = locals()
        for i in range(len(label_arr)):
            names['c%s' % i] = train_data[train_data["label"] == label_arr[i]]
        # 按类别对每个属性求均值和方差
        c_mean = []
        c_std = []
        for j in range(len(label_arr)):
            names['mc%s' % j] = []
            names['sc%s' % j] = []
            for k in range(num_feature):
                names['mc%s' % j].append(np.mean(names['c%s' % j]['%s' % k]))
                names['sc%s' % j].append(np.std(names['c%s' % j]['%s' % k], ddof=1))

        for x in range(len(label_arr)):
            c_mean.append(names['mc%s' % x])
            c_std.append(names['sc%s' % x])
            names['arr_c%s' % x] = np.array(names['c%s' % x])
        return c_mean, c_std, label_arr

    # 计算高斯概率密度函数
    @staticmethod
    def calc_gauss_prob(x, mean, stdev):
        exponent = np.exp(-(np.power(x - mean, 2)) / (2 * np.power(stdev, 2)))
        gauss_prob = (1 / (np.sqrt(2 * np.pi) * stdev)) * exponent
        return gauss_prob

    # 计算连续数据所属类的概率
    def calc_class_prob_con(self, arr, cx_mean, cx_std):
        cx_probabilities = 1
        for i in range(len(cx_mean)):
            cx_probabilities *= self.calc_gauss_prob(arr[i], cx_mean[i], cx_std[i])
        return cx_probabilities

    # 单一样本预测
    def predict(self, test_data):
        prob = []
        for i in range(len(self.mean)):
            cx_mean = self.mean[i]  # x类的均值
            cx_std = self.std[i]  # x类的方差
            prob.append(self.calc_class_prob_con(test_data, cx_mean, cx_std))  # 将计算得到的各类别概率存入列表
        best_label, best_prob = None, -1  # 初始化最可能的类和最大概率值
        for i in range(len(prob)):  # 找到所有类别中概率值最大的类
            if prob[i] > best_prob:
                best_prob = prob[i]
                best_label = self.label_array[i]
        return int(best_label), best_prob

    # 整个数据集预测
    def get_predictions(self, test_data):
        self.prediction = []
        self.test_data = np.array(test_data)
        for i in range(len(self.test_data)):
            result, prob = self.predict(self.test_data[i])
            self.prediction.append(result)
        return self.prediction

    # 计算准确性
    def get_accuracy(self):
        correct = 0
        for i in range(len(self.test_data)):
            if self.test_data[i][-1] == self.prediction[i]:
                correct += 1
        return (correct / float(len(self.test_data))) * 100.0
