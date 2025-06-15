'''
1.请输入项目根路径：project_path
2.根据根目录路径找到，res->values->string.xml文件（英文的xml文件），将多个string.xml文件路径保存起来，en_xml_path_list
  记住res的全路径，res_path
3.遍历路径en_xml_path_list
4. 将每个英文的string.xml文件【readFile(en_xml_path_list[i])】，name和value利用字典保存起来（en_dict）
5.    读取翻译文件【readFile(translate_file_name1 and 2)】,将其保存为字典 translate_dict，翻译文件放在py同级目录下
6. 如果是带id的xml，遍历en_dict，根据英文的key去找translate_dict中的value
    如果是不带id的xml文件，根据en_dict的value去找，translate_dict的key，如果完全一致，则result_dict[key] = translate[value]，或者这里可以直接打开文件写

'''
import os
import re
import xlrd
from lxml import etree

en_dict = {}
translate_dict = {}

# 校验项目根路径是否合法
def verify_path_and_exist():
    pattern = r'^(([a-zA-Z]:[\\/]|\\\\[^\\/?:*"<>|\0]+\\[^\\/?:*"<>|\0]+)[^\\/?:*"<>|\0]*(?:[\\/][^\\/?:*"<>|\0]+)*[\\/]?)$'
    regex = re.compile(pattern)
    error_msg = None
    if bool(regex.fullmatch(project_path)):
        error_msg = f'{project_path}——路径不合法'
    elif os.path.exists(project_path):
        error_msg = f'{project_path}——路径不存在'
    if error_msg is not None:
        print(error_msg)
        return False

# 获取项目根目录下，所有英文string.xml文件绝对路径
def get_en_file_path():
    # 各模块下的string_en.xml绝对路径
    en_xml_path_list = []
    # 各模块下res的绝对路径
    res_path_list = []
    # 遍历目录树
    for root, dirs, files in os.walk(project_path):
        # 检查当前目录是否是 res 目录
        if os.path.basename(root) == 'res':
            # 构建 values/string.xml 路径
            string_xml_path = os.path.join(root, 'values', 'strings.xml')
            # 检查文件是否存在
            if os.path.isfile(string_xml_path):
                en_xml_path_list.append(string_xml_path)
                res_path_list.append(root)
                print(string_xml_path)
                # print(root)
            # else:
            #     print(f"找到 res 目录但未找到 values/strings.xml: {root}")
    return en_xml_path_list, res_path_list


# 读取并解析string_en.xml
def parse_en_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        print(f'====================开始解析string_en.xml：{path}==================')
        in_string_tag = False
        for line in file:
            line = line.strip()
            if line.startswith('<string ') and line.endswith('</string>'):
                # 解析 <string> 标签
                elem = etree.fromstring(line.replace('tools:', '').replace('xliff:', ''))
                name = elem.get('name', '')
                value = elem.text if elem.text else ''
                en_dict[name] = value
                # print(f"name: {name}, value: {value}")
            elif '<string ' in line and not in_string_tag:
                in_string_tag = True  # 忽略多行 string 标签
            elif '</string>' in line:
                in_string_tag = False
            elif not in_string_tag:  # 非 <string>
                en_dict[line] = None
                # print(line)  # 直接打印原始行
    print(f'====================解析完成string_en.xml：{path}==================')

# 读取带id的翻译文件
def read_translate_xml_with_id(translate_file_path):
    wb = xlrd.open_workbook(translate_file_path)
    # wb = xlrd.open_workbook(r"xxxx.xls")
    sheet_names = wb.sheet_names()
    for i in range(len(sheet_names)):
        sheet = wb.sheet_by_name(sheet_names[i])
        rows = sheet.nrows
        columns = sheet.ncols
        for row in range(1, rows):
            temp_key = ''
            for col in range(columns):
                value = sheet.cell(row, col).value
                if col == 0:# key: ID
                    translate_dict[value] = ''
                    temp_key = value
                if col == columns - 1:# value: 翻译值
                    translate_dict[temp_key] = value

# 读取不带id的翻译文件
# def read_translate_xml_no_id():
#     translate_dict[111] = "aaaa"

# 将en_dict key 和 translate_dict key相同时，将value写入
def write_file_with_translate(fp):
    with open(fp, 'w', encoding='utf-8') as file:
        for key in en_dict:
            if key in translate_dict:
                str = f'\t<string name="{key}>${translate_dict[key]}</string>'
            elif key != '' and (key not in translate_dict) and ('<' not in key):
                str = f'\t<string name="{key}></string>'
            else:
                if 'resource' in key or 'xml' in key:
                    str = key
                else:
                    str = f'\t{key}'
            file.write(str + "\n")




project_path = input('输入项目根路径: ')
translate_file_path = ''
final_translate_path = 'string.xml'

if not verify_path_and_exist():
    en_xml_path_lists, res_path_lists = get_en_file_path()
    for en_xml_path in en_xml_path_lists:
       parse_en_file(en_xml_path)
       # read_translate_xml_with_id(translate_file_path)
       write_file_with_translate(final_translate_path)

    print("文件成功生成")