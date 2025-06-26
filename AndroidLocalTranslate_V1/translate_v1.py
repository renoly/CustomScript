# 导入 xlrd 模块
import os.path
import re
import xlrd


# 存放所有的日语文件的name
ja_names = []

# 存放excel中，string name和翻译的荷兰语
excel_key_value = {}
# excel_key_value = {"system_settings": "aaaaa", "zzzzz": "hisd"}

# 最终翻译的值
result_key_value = {}


# 1.提取日语的所有name，也就是读取ja.txt
#    <string name="bt_auto_connect_failure" tools:ignore="ExtraTranslation">Bluetooth の自動接続に失敗しました!!!</string>提取会有问题
def read_ja_names():
    ja_name_count = 0
    with open('en.xml', 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            format_name = get_name_by_string(line)
            ja_names.append(format_name)
            if format_name != '':
                ja_name_count += 1
    print('ja_names: ', ja_names)
    return ja_name_count

# 通过<string>标签取出name属性值
def get_name_by_string(str):
    pattern = re.compile('<string name="(.+)" ')
    name_list = pattern.findall(str)
    if len(name_list) > 0:
        return name_list[0]
    elif len(name_list) == 0 and str.find('<string name=') != -1:
        pattern = re.compile('<string name="(.+)">')
        return pattern.findall(str)[0]
    return ''# 字符串不是<string>标签格式


# 2.提取出excel中的id和nl键值对
def extra_excel_id_value():
    wb = xlrd.open_workbook(r"平板界面文本 string完整版(1).xls")
    sheet_names = wb.sheet_names()
    # print(sheet_names)

    for i in range(len(sheet_names)):
        sheet = wb.sheet_by_name(sheet_names[i])
        # print('-------------------------------------------------------')
        # print(sheet)

        rows = sheet.nrows
        columns = sheet.ncols
        # print(rows, columns)

        # 依次遍历所有sheet表单
        for row in range(1, rows):
            temp_key = ''
            for col in range(columns):
                value = sheet.cell(row, col).value
                if col == 0:# key: ID
                    excel_key_value[value] = ''
                    temp_key = value
                if col == columns - 1:# value: NL翻译值
                    excel_key_value[temp_key] = value


def print_dict(intro, map1):
    print(intro)
    for key in map1.keys():
        print(key, map1[key], sep='===================================')


# 3. 通过日语的key name，找出对应的荷兰语的value
def get_nl_value_by_ja_key():
    for name in ja_names:
        flag = False
        for key in excel_key_value.keys():
            nl_value = excel_key_value[key]
            if name == key:# 进入这里的nl_value则为日语key对应的荷兰语value
                result_key_value[key] = nl_value
                flag = True
                continue
                # print(key, nl_value, sep='--------------')
        if not flag:# 在excel中里没有对应的name
            result_key_value[name] = ''
    print_dict('name and translated value: ', result_key_value)

# 4. 写入文件中（nl.txt）
def write_file():
    file_name = 'nl.txt'
    count = 0
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'a', encoding='utf8') as file:
        for key in result_key_value.keys():
            if key != '':
                count += 1
                line = '<string name="' + key + '">' + result_key_value[key] + '</string>\n'
                file.writelines(line)
    return count


ja_name_count = read_ja_names()
extra_excel_id_value()
get_nl_value_by_ja_key()
count = write_file()
print('__________________________________________________________________')
print('ja_names length is: ', ja_name_count)
print('final translate len is: ', count)