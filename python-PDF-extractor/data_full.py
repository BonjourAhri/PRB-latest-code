from clean_data import clean_data
from pdfjiexi import extract_pdf
from dataformat_location import location
from dataformat_lnv import inventory
from dataformat_ht import ht
from find_ht import find_ht
from find_diam   import find_diam
from find_plate import find_plate
from dataformat_description import description
import pandas as pd
'''
按照顺序分别提取
location inventory ht diam plate description并将其合并导出为csv文件
'''
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
# print(data_loc)
# print(len(data_loc))
inv = inventory()
data_inv = inv.extract_location(x)
data_inv = inv.inventory_clean_2(data_inv)
data_inv = inv.inv_clean_RED(data_inv)
data_inv = inv.inv_clean_S(data_inv)
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
# print(data_inv)
# print(len(data_inv))
ht = ht()
data_ht = ht.extract_location(x)
data_ht = ht.ht_clean_24RED(data_ht)
data_ht = ht.ht_clean_PLATE(data_ht)
data_ht = ht.ht_clean_S(data_ht)
data = ht.pop_ht_data(data_ht)
finder = find_ht()
finder2 = find_diam()
finder3 = find_plate()
index  = finder.find_ht_index(data)
data_ht = ht.extract_ht(index,data)
index2 = finder2.find_diam_index(data)
data_diam = ht.extract_diam(index2,data)
index3 = finder3.find_plate_index(data)
data_plate = ht.extract_plate(index3,data)
# print(data_ht)
# print(len(data_ht))
# print(len(data_diam))
# print(data_diam)
# print(len(data_plate))
# print(data_plate)
des = description()
data_des = des.get_des(x)

data_list = []

for i in range(len(data_loc)):
    data_ele = []
    data_ele.append(i)
    data_ele.append(data_loc[i])
    data_ele.append(data_inv[i])
    data_ele.append(data_ht[i])
    data_ele.append(data_diam[i])
    data_ele.append(data_plate[i])
    data_ele.append(data_des[i])
    data_list.append(data_ele)

print(len(data_list))
print(data_list)
# Data columns include
# Location,Catalogue or inventory number,Provenance,Ht (= height),Plate reference,
# Vase description,Final note in entry
name_attribute = ['ID','Location','Catalogue or inventory number or Provenance','Ht (= height)','Diam','Plate reference','Description']
writerCSV=pd.DataFrame(columns=name_attribute,data=data_list)
writerCSV.to_csv('./data_final_2.csv',encoding='utf-8',index = None)