class find_plate(object):
    '''
        查询数据中所有plate的位置并返回索引
    '''
    def find_plate_index(self,data):
        indexs_plate =[]
        for i in data:
            index = i.find('PLATE')
            indexs_plate.append(index)
        return indexs_plate