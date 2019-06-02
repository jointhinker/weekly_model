#coding:utf-8
from math import log10
import codecs
import heapq
import jieba.posseg as pseg
import  sys
import os
print(sys.path)
import tag_extract
from tag_extract import sent_seg
from tag_extract import file2list
#修改类
# docList is the corpus with each element a doc, each doc is a list of words
stop = file2list(u"哈工大停用词表.txt")


def k_max_tfidf(term_tfidf):
    for id,value in term_tfidf.items():
        value_sort = sorted(value.iteritems(), key=lambda value: value[1], reverse=True)
        for i in range(5):
            print value_sort[i][0]

def tfidf_pro(doc_dict):
    type_num = len(doc_dict)
    doc_num = 0
    term_df = dict()
    for type,doc_list in doc_dict.items():
        print(type,doc_list)
        doc_num += len(doc_list)
        for doc in doc_list:
            for term in set(doc):
                if term not in term_df:
                    term_df[term] = 1.0
                else:
                    term_df[term] += 1.0

    for term in term_df:
        term_df[term] = log10(doc_num / term_df[term])
    print("doc_num:",doc_num)
    print("term_df",term_df)
    #raise KeyError
    #新创建短语的tfidf，短语赋值取自term

    #初始化phrase，遍历phrase，取每个词的tf-idf 加和
    term_tfidf = dict()
    for type,doc_list in doc_dict.items():
        term_tfidf[type] = dict()
        term_tf = dict()
        term_num = 0
        for doc in doc_list:
            term_num += len(doc)
            for term in doc:
                if term not in term_tf:
                    term_tf[term] = 1.0
                else:
                    term_tf[term] += 1.0

        for doc_id, doc in enumerate(doc_list):
            term_tfidf[type][doc_id] = dict()
            for term in doc:
                tfidf = term_tf[term] / term_num * term_df[term]
                term_tfidf[type][doc_id][term] = tfidf
    #print(term_tfidf)
    return term_tfidf
def notNumStr(instr):
    #识别是否出现a-z A-Z 数字 。可用正则替换
    for item in instr:
        if '\u0041' <= item <= '\u005a' or ('\u0061' <= item <='\u007a'):
            #or item.isdigit():
            return False
    return True

def get_phrase_tfidf(term_tfidf,doc_dict_origin):
    #print("doc_dict_origin",doc_dict_origin)
    swLibList = []
    #poSPrty = ['x', 'uj', 'ul', 'mq', 'u', 'v', 'f']
    poSPrty=[]
    #3 num ->m
    phrase_tfidf = dict()
    for type, doc_list in doc_dict_origin.items():
        print("doc_dict_origin",type,doc_list)
        meaningfulCount = 0
        phrase_tfidf[type] = dict()
        for index, doc in enumerate(doc_list):
            #print(type)
            doc = doc +"\n"
            phrase_tfidf[type][index] = dict()
            rawtextList = pseg.cut(doc)
            startphrase = ""
            for eachWord, flag in rawtextList:
                print("eachWord")
                print(eachWord)
                #print(flag)
                # 如果分词 在短语停用词列表中 或者 为 字母、数字 或者 是停用词 或者 词性为 需要丢弃的无用词 或者 为换行符
                if eachWord in stop or not notNumStr(eachWord) or eachWord in swLibList or flag in poSPrty or eachWord == '\n':
                    #若该短语不在字典中，初始化
                    if not startphrase :
                        #避免开始短语是空
                        continue
                    #print("eachword discard")
                    print("startphrase")
                    print(startphrase)
                    if " " in startphrase:
                        words = startphrase.split(" ")
                    else:
                        words = [startphrase]

                    #过滤条件，短语长度超过4 短语字符长度<=2
                    if len(words) > 4 or len(startphrase)<=2 :
                        startphrase = ""
                        continue
                    if startphrase not in phrase_tfidf[type][index]:
                        phrase_tfidf[type][index][startphrase] = 0
                    #如果是停用词，将之前的短语分隔后分别得到tfidf，加和求权，赋值到短语tfidf上。并且startword初始化

                    for item_word in words:
                        phrase_tfidf[type][index][startphrase] += term_tfidf[type][index].get(item_word,0)
                    startphrase = ""

                # 如果分词 不在停用词 中  并且不是换行符
                else:
                    #如果该词不是停用词，则拼接短语
                    if startphrase:
                        startphrase += " "+eachWord
                    else:
                        startphrase = eachWord
                    meaningfulCount += 1
    return phrase_tfidf

def create_data(dir_path, doc_type=None):
    doc_dict = {}
    for maindir, subdir, file_name_list in os.walk(dir_path):
        for file in file_name_list:
            file_name = file.split(".")[0]
            doc_dict[file_name] = []
            apath = os.path.join(maindir, file)
            with codecs.open(apath,"r","utf-8") as f:
                lines = [l.strip() for l in f.readlines()[:20]]
                if doc_type:
                    #存储形式为 {type:[doc1,doc2,doc3]}，文档不做处理
                    doc_dict[file_name] = lines
                else:
                    #文档做处理，{type:[["word1","word2"],[]]}
                    doc_dict[file_name] = sent_seg(lines, stop, "list")
    return doc_dict

if __name__ == "__main__":
    dir_path = "corpus"
    doc_dict = create_data(dir_path)
    doc_dict_origin = create_data(dir_path, "origin")
    print("doc_dict_origin",doc_dict_origin)
    term_tfidf = tfidf_pro(doc_dict)
    phrase_tfidf = get_phrase_tfidf(term_tfidf,doc_dict_origin)

    for type, doc_list in doc_dict.items():
        print type
        for index, item in enumerate(doc_list):
            print(doc_dict_origin[type][index])
            value = phrase_tfidf[type][index]
            value_sort = sorted(value.iteritems(), key=lambda value: value[1], reverse=True)
            for i in range(8):
                if i < len(value_sort):
                    print "".join(value_sort[i][0].split(" "))
