class find_ht(object):
    '''
        查询数据中所有ht的位置并返回索引
    '''
    def find_ht_index(self,data):
        indexs_ht =[]
        for i in data:
            index = i.find('Ht')
            indexs_ht.append(index)
        return indexs_ht
    def find_ht_index2(self, data):
        indexs_ht = []
        for i in data:
            index = i.find('ht')
            indexs_ht.append(index)
        return indexs_ht