#
# Data columns include
# Location,Catalogue or inventory number,Provenance,Ht (= height),Plate reference,
# Vase description,Final note in entry

#Catalogue or inventory number and proven
from clean_data import clean_data
from pdfjiexi import extract_pdf
from find_ht import find_ht
from find_diam   import find_diam
from find_plate import find_plate
import re
'''
inventory类 负责定位，提取，清理已经提取出的pdf文本中的inventory信息
'''
class  inventory(object):

    def extract_location(self,x):
        '''
        :param x: 被提取出来的pdf 生文本数据
        :return: 被大概定位的未清理的inventory数据(这里只能根据想要提取的条目做大致的定位)
        客户可以根据自己的需求重新对正则表达式进行设计
        这里使用的正则表达式已被作者检验过效果最佳，如果客户有其他想法可以进行修改和尝试。
        '''
        p = re.compile(r'[0-9]{1,2}  [A-Z a-z]*[ ,]([\w .()=]*)')#利用正则表达式对提取出来的pdf生数据中的inventory做粗定位
        inventory = []
        for data_location in p.findall(x):
            inventory.append(data_location)
            # print(len(location))
            # print(location)
        return inventory
    def inventory_clean_2(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于inventory信息的明显垃圾条目，例如2，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == '2':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
    def inv_clean_S(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于inventory信息的明显垃圾条目S. Agata 66，例如，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == 'S. Agata 66':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
    def inv_clean_RED(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于inventory信息的明显垃圾条目RED，例如，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == 'RED':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
    def clean_ht(self,index,data):
        '''
        :param index: 数据中ht的位置
        :param data: 未清理的数据
        :return: 被清理掉ht的数据
        '''
        new_data = []
        for i,a in enumerate(index):
            if a != -1:
                d = data[i][:a]
                new_data.append(d)
            else:
                d = data[i]
                new_data.append(d)
        return new_data
if __name__ == '__main__':
    epdf = extract_pdf()
    x = epdf.get_pdf()
    inv = inventory()
    data_inv = inv.extract_location(x)
    data_inv = inv.inventory_clean_2(data_inv)
    data_inv = inv.inv_clean_RED(data_inv)
    data_inv = inv.inv_clean_S(data_inv)
    print(data_inv)
    finder = find_ht()
    finder2 = find_diam()
    finder3 = find_plate()
    index = finder.find_ht_index(data_inv)
    data_inv = inv.clean_ht(index,data_inv)
    index2 = finder.find_ht_index2(data_inv)
    data_inv = inv.clean_ht(index2, data_inv)
    index3 = finder2.find_diam_index(data_inv)
    data_inv = inv.clean_ht(index3, data_inv)
    index4 = finder3.find_plate_index(data_inv)
    data_inv = inv.clean_ht(index4, data_inv)
    print(data_inv)
    print(len(data_inv))



