import string
'''
一些简单的字符串清理的函数的封装
'''
class clean_data(object):
    def r_strip(self,data):
        data_cleaned = []
        for i in data:
            i = i.rstrip()
            data_cleaned.append(i)
        return data_cleaned
    def r_strip_uppercase(self,data):
        data_cleaned = []
        for i in data:
            i = i.rstrip(string.ascii_uppercase)
            data_cleaned.append(i)
        return data_cleaned
    def r_strip_com(self,data):
        data_cleaned = []
        for i in data:
            i = i.rstrip(',')
            data_cleaned.append(i)
        return data_cleaned

