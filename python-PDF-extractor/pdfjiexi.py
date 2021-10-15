import logging
import os
import re
import pdfplumber
'''
使用pdfplumber库函数提取pdf中的全部文本信息
'''
class extract_pdf(object):
    def get_pdf(isText=True):
        pdf_content = '' #声明提取的pdf文本
        for _ in range(3):
            try:
                local_dir = os.getcwd() #获取当前目录路径
                print("local_dir: " + local_dir)
                file_name = '{}/RVP.pdf'.format(local_dir) #合成提取文件的绝对路径
                #pdf 解析----------------------
                pdf = pdfplumber.open(file_name)
                pages = pdf.pages[55:70] #设置提取页码，注只能从55页开始提取。
                page_num = 0
                file_obj = []
                for page in pages:
                    page_num += 1
                    # isText判断了--输入的要求是要文字/表格
                    if isText:
                        txt_tmp = page.extract_text()
                        if txt_tmp:
                            pdf_content += txt_tmp
                        else:
                            for table in page.extract_tables():
                                for row in table:
                                    rows = []
                                    for col in row:
                                        rows.append(re.sub('\n', '', str(col)))
                                    file_obj.append(rows)
                    if not isText:  # 如果要表格，则返回列表
                        return file_obj

                # pdf.close()
                # os.remove(file_name)  # 读取文件后就删除掉文件
                return pdf_content
            except Exception as e:
                logging.error('{}'.format(e))
        return ''
if __name__ == '__main__':
    epdf = extract_pdf()
    x = epdf.get_pdf()
    print(x)
    x = x.split('\n')
    print(x)