from pdfjiexi import extract_pdf
from dataformat_location import location
'''
定位提取description数据
'''
class description(object):
    def get_des(self,x):
        loc = location()
        data_loc = loc.extract_location(x)
        data_loc = loc.location_clean_and(data_loc)
        data_loc = loc.location_clean_the(data_loc)
        data_loc = loc.location_clean_plate(data_loc)
        des_index_list = []
        x = x.split('\n')
        #按照提取出的location数据对应到提取出的所有数据的具体行索引位置
        for data in x:
            for i in data_loc:
                if i in data:
                    des_index = x.index(data)
                    des_index_list.append(des_index)
        #去除重复出现的行索引
        des_index_list = set(des_index_list)
        des_index_list_new = []
        #对行索引排序
        for i in des_index_list:
            des_index_list_new.append(i)
        des_index_list_new.sort()
        des_full = []
        #将每两个行索引，即每个花瓶描述的第一行信息之间的数据提取出来作为描述信息
        for i in range(len(des_index_list_new) - 1):
            descriiption = []
            for j in range(des_index_list_new[i] + 1, des_index_list_new[i + 1]):
                descriiption.append(x[j])
            des_str = ''.join(descriiption)
            # print(des_str)
            # print('---')
            des_full.append(des_str)

        # print(des_index_list_new)
        # print(len(des_index_list_new))
        return des_full
if __name__ == '__main__':

    epdf = extract_pdf()
    x = epdf.get_pdf()
    print(x)
    des = description()
    list = des.get_des(x)
    print(list)

