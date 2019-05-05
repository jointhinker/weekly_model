#coding:utf-8
import csv
from numpy import *
import time

def normalize(data):
    m,n = data.shape
    for i in range(m):
        for j in range(n):
            if data[i,j] != 0:
                data[i,j] = 1
    return data

def load_Train():
    with open('train.csv') as file:
        data_array = []
        lines = csv.reader(file)
        for line in lines:
            line = [int(l) for l in line]
            data_array.append(line)
        data_array = array(data_array[1:])

        print data_array
        label = data_array[:,0]
        data = data_array[:,1:]

        return label,normalize(data)

def load_Test():
    with open('test.csv') as file:
        data_array = []
        lines = csv.reader(file)
        for line in lines:
            line = [int(l) for l in line]
            data_array.append(line)
        data_array = array(data_array[1:])
        return normalize(data_array)

def knn(tmp, data ,label,k):
    m = data.shape[0]
    #为计算方便，单向量复制m行后组成新的array数组
    new = tile(tmp,(m,1))
    distance = (data - new)**2
    #按列相加后开方
    result = sqrt(distance.sum(axis = 1))
    #排序按照从小到大，获取索引值，以获取label。统计前k小数据里的label个数
    index = argsort(result)
    label_dict = {}
    #字典初始化
    for i in range(k):
        label_dict[label[index[i]]] = label_dict.get(label[index[i]],0)+1
    #字典排序按照值从大到小
    return sorted(label_dict.iteritems(), key = lambda i : i[1],reverse = True)[0][0]

def test_knn():
    group = array([[1., 1.1],[1.,1.],[0.,0.],[0,0.1]])
    labels = ['A','A','B','B']
    print knn(array([[0,0]]), group, labels, 3)


#将array数组形式的label转换成列表，行向量
def toline(label):
    l_list = []
    for l in label:
        l_list.extend(list(l))
    return l_list

def train():
    label,train_data = load_Train()
    #train_data可以降维对比
    label_line = toline(label)
    test_data = load_Test()
    m = test_data.shape[0]
    test_result = []
    test_book = loadTestResult()
    #计算错误率
    errorCount= 0
    for i in range(m):
        result = knn(test_data[i], train_data, label_line, 5)
        #对比错误率
        if result != test_book[i]:
            errorCount += 1
        test_result.append(result)
    print float(errorCount)/m
    return test_result

def loadTestResult():
    l=[]
    with open('knn_benchmark.csv') as file:
         lines=csv.reader(file)
         for line in lines:
             line = [int(l) for l in line]
             l.append(line)
     #28001*2
    l.remove(l[0])
    label=array(l)
    #取array数组第一列
    return label[:,1]

def write_result(result):
    with open('result.csv','wb') as file:
        #写第一行
        mywriter = csv.writer(file)
        mywriter.writerow(['ImageId','Label'])
        index  =1
        for r in result:
            mywriter.writerow([index,r])
            index += 1
'''
def test_write_result():
    result = [2,2,3,4]
    write_result(result)

test_write_result()'''
def pca_train():
    label,train_data = load_Train()
    #train_data可以降维对比
    train_pca,para = pca(train_data)

    label_line = toline(label)
    test_data = load_Test()
    #降维
    test_pca = (test_data - para[0])*para[1]
    m = test_data.shape[0]
    test_result = []
    test_book = loadTestResult()
    #计算错误率
    errorCount= 0
    for i in range(m):
        #降维后的数据
        result = knn(test_pca[i], train_pca, label_line, 5)
        #对比错误率
        if result != test_book[i]:
            errorCount += 1
        test_result.append(result)

    print float(errorCount)/m
    return test_result

if __name__ == "__main__":
    #test_knn()
    # knn分类
    #train()
    #结合pca降纬，knn分类
    pca_train()
    










