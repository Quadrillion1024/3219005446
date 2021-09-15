#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 3219005446 姜珺杨19信息安全1班
# 编译软件用的个人习惯的jupyter notebook，有分段运行所以可能导致commit的版本比较诡异
# 软件工程个人项目 论文查重


# In[1]:

import jieba
import gensim
import sys
import numpy as np
import re
import os

# In[2]:

# # 测试版本的自用文件路径

# s1 = r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig.txt'
# s2 = r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig_0.8_dis_15.txt'
# stopwords=[]

# 利用jieba分词，将词分好并保存到向量中
# s1_cut = [i for i in jieba.cut(s1, cut_all=True) if (i not in stopwords) and i!='']
# s2_cut = [i for i in jieba.cut(s2, cut_all=True) if (i not in stopwords) and i!='']
# word_set = set(s1_cut).union(set(s2_cut))

# In[4]:

#非测试版本的获取文件路径
#其实是命令行版本
def get_file_contents(path):
    string = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        string = string + line
        line = f.readline()
    f.close()
    return string

# In[3]:

#将读取到的文件内容先把标点符号、转义符号等特殊符号过滤掉，然后再进行结巴分词
#jieba.luct生成list
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    '''
    result_text = jieba.lcut(string)
    '''
    return string

# In[3]:
    '''
def filter(string):
	result_text = []
	pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")   #定义正则表达式匹配模式
	data = pattern.sub("",string)  # 只保留英文a-zA-z、数字0-9和中文\u4e00-\u9fa5的结果。	去除标点符号
	result_text = [i for i in jieba.cut(data, cut_all=False) if i != '']  #分词
	return result_text
    '''
# In[6]:
#待优化的余弦相似度
#传入过滤数据
'''
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
'''
# In[]
def get_word_vector(s1,s2):
    """
    :param s1: 句子1
    :param s2: 句子2
    :return: 返回句子的余弦相似度
    """
    # 分词
    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1
    return word_vector1, word_vector2


# In[]
def calc_similarity(vec1,vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    dist1=float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    return dist1

# In[5]:

def main_test(text1_abs_path,text2_abs_path):
    
    str1 = get_file_contents(text1_abs_path)
    str2 = get_file_contents(text2_abs_path)
    text1 = filter(str1)
    text2 = filter(str2)
    vec1,vec2=get_word_vector(text1,text2)
    similarity = calc_similarity(vec1, vec2)   
    result=round(similarity,4) 
    #四舍五入
    result=result*100
    return result
# In[ ]:

#命令行版本的获取文件路径
if __name__ == '__main__':
 
    text1_abs_path = sys.argv[1]
    text2_abs_path = sys.argv[2]
    save_abs_path = sys.argv[3]
#命令行参数传入：main.py、[论文原文的文件的绝对路径]、[抄袭版论文的文件的绝对路径]、[输出的答案文件的绝对路径]
    result=main_test(text1_abs_path,text2_abs_path)
    
    print("文章相似度： %.2f" % result)
    #将相似度结果写入指定文件
    f = open(save_abs_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.2f"% result)
    f.close()


