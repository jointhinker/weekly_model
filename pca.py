#coding:utf-8
from numpy import *
def pca(data_mat, topN_feat=-1):
    mean_vals = mean(data_mat, axis = 0)
    mean_differ = data_mat - mean_vals
    print mean_differ
    cov_mat = cov(mean_differ, rowvar=0)
    eig_midst_vals, eig_midst_vects = linalg.eig(mat(cov_mat))
    #从小到大
    eig_val = argsort(eig_midst_vals)
    print eig_midst_vals,eig_val

    value = sum(eig_midst_vals**2)*0.9
    eig_midst_vals_ener = eig_midst_vals**2
    length = len(eig_val)
    sum_val = 0
    for i in range(length):
        sum_val += eig_midst_vals_ener[eig_val[length-1-i]]
        if sum_val>= value:
            break
    top = i+1
    #print top,'top'
    #未赋初始值时设为top
    if topN_feat == -1:
        topN_feat = top
    eig_val = eig_val[:-(topN_feat+1):-1]
    red_vects = eig_midst_vects[:,eig_val]
    #降维后的数据
    low_data_mat = mean_differ * red_vects
    #降维前的数据，因为在计算降维后的数据时取的近似值，所以计算原数据矩阵会不一致，大致一样
    return low_data_mat,(mean_vals, red_vects)

if __name__ =='__main__':
    data_mat = array([[1,1,],[1,3],[2,3],[4,4],[2,4]])
    data_pca, para = pca(data_mat,1)
    print '降维后的数据',data_pca
    #print '测试集降维',(array([[1,1],[1,3]])-para[0])*para[1]