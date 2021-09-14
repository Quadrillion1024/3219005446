#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 3219005446 姜珺杨19信息安全1班
# 编译软件用的个人习惯的jupyter notebook，有分段运行所以可能导致commit的版本比较诡异
#在第二版本为了方便命令行操作已经转去加入spyder啦
# 软件工程个人项目 论文查重


# In[1]:

import jieba
import gensim
import sys
import re
import os

# In[2]:


# # 测试版本的自用文件路径

# s1 = r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig.txt'
# s2 = r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig_0.8_dis_15.txt'
# stopwords=[]

# In[3]:
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
    result = jieba.lcut(string)
    return result
 


# In[6]:


#传入过滤数据,余弦相似度 1
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
 

# In[5]:


def main_test(text1_abs_path,text2_abs_path):
    
    str1 = get_file_contents(text1_abs_path)
    str2 = get_file_contents(text2_abs_path)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)   #生成的similarity变量类型为<class 'numpy.float32'>
    result=round(similarity.item(),2)  #借助similarity.item()转化为<class 'float'>，然后再取小数点后两位
    result=result*100
    return result


# In[8]:

# print("文本相似度为：%.2f%%"%main_test())

# In[ ]:


#命令行版本的获取文件路径 参数传入：main.py、[论文原文的文件的绝对路径]、[抄袭版论文的文件的绝对路径]、[输出的答案文件的绝对路径]
if __name__ == '__main__':
 
    text1_abs_path = sys.argv[1]
    text2_abs_path = sys.argv[2]
    save_abs_path = sys.argv[3]
    result=main_test(text1_abs_path,text2_abs_path)
    
    print("文章相似度： %.2f" % result)
    #将相似度结果写入指定文件
    f = open(save_abs_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.2f"% result)
    f.close()


