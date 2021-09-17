#!/usr/bin/env python
# coding: utf-8


# 3219005446 姜珺杨19信息安全1班
# 编译软件用的个人习惯的jupyter notebook，有分段运行所以可能导致commit的版本比较诡异
# 软件工程个人项目 论文查重

import jieba
import gensim
import sys
import time
import re
import os


def get_file_contents(path):
    string = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        string = string + line
        line = f.readline()
    f.close()
    return string

def filter(string):
	result_text = []
	pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")   #定义正则表达式匹配模式
	data = pattern.sub("",string)  # 只保留英文a-zA-z、数字0-9和中文\u4e00-\u9fa5的结果。	去除标点符号
	result_text = [i for i in jieba.cut(data, cut_all=False) if i != '']  #分词
	return result_text


#传入过滤数据

def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim

def main_test(text1_abs_path,text2_abs_path):
    
    str1 = get_file_contents(text1_abs_path)
    str2 = get_file_contents(text2_abs_path)   #获得文本
    text1 = filter(str1)
    text2 = filter(str2)   #过滤
    similarity = calc_similarity(text1, text2)   #计算
    result=round(similarity,4)   #四舍五入
    result=result*100
    return result

#命令行版本的获取文件路径
if __name__ == '__main__':
#    start = time.time()
    text1_abs_path = sys.argv[1]
    text2_abs_path = sys.argv[2]
    save_abs_path = sys.argv[3]
#异常处理部分
    if not os.path.exists(text1_abs_path) :
        print("论文原文文件不存在！")
        exit()
    if not os.path.exists(text2_abs_path):
        print("抄袭版论文文件不存在！")
        exit()
    if not os.path.exists(save_abs_path):
        print("答案文件文件不存在！")
        exit()    
    if text1_abs_path.endswith('.txt')==False:
        print("原文文件格式错误!")
        exit()
    if text2_abs_path.endswith('.txt')==False:
        print("抄袭版论文文件格式错误!")
        exit()
    if save_abs_path.endswith('.txt')==False:
        print("生成文件格式错误!")
        exit()
    if os.path.getsize(text1_abs_path) == 0:
        print("论文原文文件是空的")
    if os.path.getsize(text2_abs_path) == 0:
        print("抄袭版论文文件是空的")
        
#命令行参数传入：main.py、[论文原文的文件的绝对路径]、[抄袭版论文的文件的绝对路径]、[输出的答案文件的绝对路径]
    result=main_test(text1_abs_path,text2_abs_path)   
    #在命令行的时候显示结果
    print("文章相似度： %.2f" % result)
    #将相似度结果写入指定文件
    f = open(save_abs_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.2f"% result)
    f.close()
#    end = time.time()
#    print("运行总时间:",end-start)
    

