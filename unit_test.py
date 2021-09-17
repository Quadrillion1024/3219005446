# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 20:23:25 2021

@author: Quadrillion
"""

import unittest
from main import main_test
from main import get_file_contents


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig.txt',r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig_0.8_dis_1.txt'),99.83000159263611)
#unittest2 文件0000为我编写的空txt文件
class MyTestCase2(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(r'C:\Users\Quadrillion\Desktop\01\测试文本2\0000.txt',r'C:\Users\Quadrillion\Desktop\01\测试文本2\orig_0.8_dis_1.txt'),0)
#unittest2 文件0001内容为"无事发生"
class MyTestCase3(unittest.TestCase):
    def test_something(self):
        self.assertEqual(get_file_contents(r'C:\Users\Quadrillion\Desktop\01\测试文本2\0001.txt'),"无事发生")
if __name__ == '__main__':
    unittest.main() 