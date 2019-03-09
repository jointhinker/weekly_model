#coding:utf-8
from numpy import *
#加载文档词向量数据以及相应文档类别，0表示正常言论，1表示侮辱性文字
def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                   ['maybe','not','take','him','to','dog','park','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']
        ]
    classVec = [-1,1,-1,1,-1,1]
    return postingList,classVec


def createVocabList(dataSet):
    '''
    功能：将已知类别文档中出现的词汇 存入到 所有词汇集合，相当于字典 返回其list类型

    输入数据类型：列表类型（列表中存储的是列表元素，每篇文档的词汇集合）
    输出数据类型：列表类型（字典）
'''
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList,inputSet):
    '''
    功能：将输入的文档转成词向量形式，即在字典中所有词汇出现的词频数，出现为1，未出现为0.
    输入数据类型：列表类型（字典，存储所有词汇）
                  字符串（将要预测的留言）
    输出数据类型：列表类型（词向量）

'''
    returnVec =[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            #当输入的词不在词典中的话，则可以引用同义词的概念，来填充词向量
            print "the word : %s is not in my Vocabulary!" % word
    return returnVec



#在此函数上引用权重D，使得每个训练向量都能与权重对应相乘
def trainNB0(trainMatrix, trainCategory,D):
    '''
    功能：计算属于1类对应下的所有词汇出现的词频数（词向量形式），用p1Num存放。0类一样。
          计算属于1类的所有词汇总数，用p1Denom存放。0类一样。
          返回字典词汇的条件概率p0Vect,p1Vect以及文档属于1类的概率pAbusive。p0Vect= [p(w1|c1),p(w2|c1)...p(wn|c1)]

    输入的数据类型：array列表类型（样本词向量）
                    array列表类型（样本对应的类别）
    输出的数据类型：列表类型（字典词汇的条件概率0）
                    列表类型（字典词汇的条件概率1）
                    浮点数（文档属于1类的概率）
'''
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    #计算属于1类的先验概率
    pAbusive = sum([t for t in trainCategory if t!=-1])/float(numTrainDocs)
    #初始化频数全部为1，防止有的单词后验概率为0，使用log来防止下溢，即后验概率不能为0。下面是-1和1类两种
    p0Num = ones(numWords)
    p1Num = ones(numWords)

    p0Denom = 2.0
    p1Denom = 2.0
    #使对应位置相乘，变成权重向量
    trainMatrix_D = trainMatrix * array(D)
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            #数学技巧,因为p1Num初始为1，所以乘以权重后，和最初未计算权重时的结果不相符。这里需要考虑一个问题就是初始化频数为1默认的是不是太大，因为词向量乘以权重初始为0.几
            p1Num += trainMatrix_D[i]
            p1Denom += sum(trainMatrix_D[i])
        else:
            p0Num += trainMatrix_D[i]
            p0Denom += sum(trainMatrix_D[i])

    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive



def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    '''
    功能：计算贝叶斯概率公式，忽略分母（因为每个类别的分母相等）。计算技巧是分子变形，使相乘的n个数转换为log每个数相加
          返回留言板的预测类别。

    输入数据类型：列表（词向量形式）
                  列表（字典词汇的条件概率0）
                  列表（字典词汇的条件概率1）
                  浮点数（文档属于1类的概率）
    输出数据类型：整数（预测类别）
'''
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1>p0:
        return 1
    else:
        return -1

def tesingNB(dataMat,classLabels,numIt=40):
    '''
    功能：功能：调用以上定义的功能函数，训练分类器然后测试两条数据,调用以上定义的功能函数，训练分类器然后测试两条数据
'''
    trainMat, listClasses = dataMat,classLabels
    labelMat = mat(listClasses).T
    #print labelMat
    #几行几列
    n = len(trainMat[0])
    m = len(trainMat)
    #改动做实验
    D = mat(ones((m, 1)) / m)#初始化所有样本的权值一样
    aggClassEst = mat(zeros((m, 1)))  # 每个数据点的估计值
    weakClassArr = []
      #从这部分开始结合权重迭代出贝叶斯分类器参数

    for i in range(numIt):
        bestStump = {}
        #结合adaboost时需要传入词向量的权重。需要训练迭代若干次，在这部分需要加上预测的类别以及错误率（使用权重计算）。
        p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses),D)
        bestStump['p0V']=p0V
        bestStump['p1V'] = p1V
        bestStump['pAb'] = pAb
        #print p0V,p1V,pAb
        #预测训练集合的类别
        predictedVals = []
        for t in trainMat:
            print t
            predictedVals.append(classifyNB(t, p0V, p1V, pAb))
        #只有array数组才能进行运算后期和 alpha相乘
        predictedVals = array([predictedVals]).T
        errArr = mat(ones((m, 1)))
        errArr[predictedVals == labelMat] = 0
        weightedError = D.T * errArr
        alpha = float(0.5 * log((1.0 - weightedError) / max(weightedError, 1e-16)))
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)

        expon = multiply(-1 * alpha * labelMat, predictedVals)
        D = multiply(D, exp(expon))
        D = D / D.sum()

        aggClassEst += alpha * predictedVals
        aggErrors = multiply(sign(aggClassEst) != labelMat, ones((m, 1)))
        errorRate = aggErrors.sum() / m
        print "total error: ", errorRate
        if errorRate == 0.0:
            break
    return weakClassArr

def adaClassify(datToClass,classifierArr):
    dataMatrix = datToClass
    #在此注意dattoClass类型,这边容易犯的错误是传入classifyNB函数的接口参数数据集应该是array列表形式，元素为数值。即单个向量。
    print 'dataMatrix',dataMatrix
    aggClassEst=0
    for i in range(len(classifierArr)):
        #总分类器中的每个弱分类器是已知的最佳弱分类器，参数都已定好。直接调用stumpClassify函数进行分类，并输出预测结果classEst
        classEst = classifyNB(dataMatrix,classifierArr[i]['p0V'],classifierArr[i]['p1V'], classifierArr[i]['pAb'])#call stump classify
        #利用预测结果以及弱分类器的alpha值，算出单个的结果，然后循环算出总分类器f(x)值
        aggClassEst += classifierArr[i]['alpha']*classEst
    #取结果值得符号
    return sign(aggClassEst)

def main():
    #加载数据，赋初始值样本权重为相等的 1/样本数
    dataMat,classLabels = loadDataSet()
    myVocabList = createVocabList(dataMat)
    trainMat=[]
    for postinDoc in dataMat:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    #classifierArr存放：总分类器，元素为弱分类器的详细情况
    classifierArr = tesingNB(trainMat,classLabels,30)
    print len(classifierArr)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print 'thisDoc',thisDoc
    t = adaClassify(thisDoc, classifierArr)
    print t

if __name__ == "__main__":
    main()
