class find_diam(object):
    '''
        查询数据中所有diam的位置并返回索引
    '''
    def find_diam_index(self,data):
        indexs_diam =[]
        for i in data:
            index = i.find('Diam')
            indexs_diam.append(index)
        return indexs_diam