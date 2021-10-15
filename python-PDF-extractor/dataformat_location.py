#
# Data columns include
# Location,Catalogue or inventory number,Provenance,Ht (= height),Plate reference,
# Vase description,Final note in entry

#Location
from clean_data import clean_data
from pdfjiexi import extract_pdf
import re
'''
location类 负责定位，提取，清理已经提取出的pdf文本中的location信息
'''
class location(object):
    def extract_location(self,x):
        '''
        :param x: 被提取出来的pdf 生文本数据
        :return: 被大概定位的未清理的位置数据(这里只能根据想要提取的条目做大致的定位)
        客户可以根据自己的需求重新对正则表达式进行设计
        这里使用的正则表达式已被作者检验过效果最佳，如果客户有其他想法可以进行修改和尝试。
        '''
        p = re.compile(r'[0-9]{1,2}  ([A-Z a-z]*[ ,])') #利用正则表达式对文本中的location内容做大致定位
        location = [] #储存被大致定位的位置信息
        for data_location in p.findall(x):
            location.append(data_location)
            # print(len(location))
            # print(location)
        return location
    def location_clean_the(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于location信息的明显垃圾条目，例如THE，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == 'THE ':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
    def location_clean_plate(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于location信息的明显垃圾条目，例如PLATE，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == 'PLATE ':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
    def location_clean_and(self,location):
        '''
        :param location: 被大概定位的未清理的位置信息
        :return: 清理不属于location信息的明显垃圾条目，例如and，返回清理后的数据
        '''
        # location = extract_location(x)
        length = len(location)
        index = 0
        while index < length:
            if location[index] == 'and ':
                del location[index]
                index-=1
                length -= 1
            index+=1
        return location
if __name__ == '__main__':
    epdf = extract_pdf()
    x = epdf.get_pdf()
    loc = location()
    data_loc = loc.extract_location(x)
    data_loc = loc.location_clean_and(data_loc)
    data_loc =  loc.location_clean_the(data_loc)
    data_loc = loc.location_clean_plate(data_loc)
    data_cleaner = clean_data()
    data_loc = clean_data.r_strip(data_cleaner,data=data_loc)
    data_loc = clean_data.r_strip_uppercase(data_cleaner,data_loc)
    data_loc = clean_data.r_strip_com(data_cleaner,data_loc)
    data_loc = clean_data.r_strip(data_cleaner, data=data_loc)
    print(data_loc)
    print(len(data_loc))


