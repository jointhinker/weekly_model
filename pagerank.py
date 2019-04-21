#coding:utf-8

import re
import sys
from operator import add
from pyspark import SparkConf, SparkContext

def compute_contribs(urls, rank):
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)

def compute_pagerank(sc, url_data_file, iterations):
    # 数据格式如下 1 2
    lines = sc.textFile(url_data_file).map(lambda line: line.encode('utf8'))
    links = lines.map(lambda line: line.split(" ")).distinct().groupByKey().mapValues(lambda x: list(x)).cache()
    ranks = lines.map(lambda line: (line[0], 1))

    for i in range(iterations):
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: compute_contribs(url_urls_rank[1][0], url_urls_rank[1][1]))
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.75 + 0.25)

    for (link, rank) in ranks.collect():
        print("%s has rank %s." % (link, rank))
    return 0


if __name__ == '__main__':
    # 数据文件和迭代次数
    url_data_file = sys.argv[1]
    iterations = int(sys.argv[2])
    # 配置 SparkContext
    conf = SparkConf().setAppName('PageRank')
    conf.setMaster('local')
    sc = SparkContext(conf=conf)
    ret = compute_pagerank(sc, url_data_file, iterations)
