import os
import re
import shutil
import zipfile
from bai_api import translate
import logging


def rw_file(file_path, model, tr_con=''):
    with open(file_path, model, encoding='utf-8') as f:
        if model == 'r':
            # 读取并返回文件内容
            return f.read()
        elif model == 'w':
            f.write(tr_con)
            f.close()


def zip_dir(directory, zipname):
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                outZipFile.write(filepath, filename)

        outZipFile.close()


# # 检索整合包
packages = os.listdir('package')

# package文件夹,删除非.zip格式以外的文件,请不要在package存放任何与整合包无关的文件夹/文件
for file in packages:
    if os.path.splitext(file)[1] != '.zip':
        shutil.rmtree('package\\' + file)

# 重新检索整合包
packages = os.listdir('package')

# ftbquests路径
fq = '\\overrides\\config\\ftbquests'
# 翻译完成的整合包路径
tr_package = 'tr_package\\'

logging.basicConfig(level=logging.INFO, format='%(message)s', filename='trLog.log', filemode='a')

# 解压整合包
for package in packages:
    # 获取整合包的名字,后续用作解压路径
    package_path = 'package\\' + os.path.splitext(package)[0]
    # 整合包对应的ftbquests路径
    fq_path = package_path + fq
    # 解压整合包至相应文件夹
    with zipfile.ZipFile('package\\' + package) as unzip:
        unzip.extractall(package_path)
        unzip.close()

    # # 如果存在ftbquests文件,则进行文件检索并翻译
    if os.path.exists(fq_path):
        for i in os.listdir(fq_path):
            quests_file_path = fq_path + '\\' + i + '\\chapters\\'
            # 检索ftbquests文件路径
            files_name = os.listdir(quests_file_path)
            # ftbquests的文件翻译
            for q in files_name:
                logging.info('开始翻译文件:' + q)
                logging.info('-' * 20)
                print('开始翻译文件:' + q)

                q_path = quests_file_path + q
                content = rw_file(q_path, 'r')
                # print(content)

                # 正则 消除MC的格式化代码样式
                # 详情参考 https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81
                content_cut = re.sub('&\w', '', content)
                # 正则 寻找title和subtitle中的翻译内容
                title_langs = re.findall('[sub]*title: \"(.*)\"', content_cut)
                # print(title_langs)

                # 翻译内容并覆写原文件
                for title in title_langs:
                    tr_l = translate(title)
                    content_cut = content_cut.replace(title, tr_l, 1)
                    logging.info(title)
                    logging.info(tr_l)
                    logging.info('-' * 20)

                disp_all = re.findall('\tdescription: \[([\s\S]*?)]', content_cut)
                disp_langs = []
                for d in disp_all:
                    disp_s = re.findall('\"(.*)\"', d)
                    for di in disp_s:
                        if di != '' and len(re.findall('width|height|align', di)) != 3:
                            disp_langs.append(di)

                for disp in disp_langs:
                    tr_l = translate(disp).replace('\\', '')
                    content_cut = content_cut.replace(disp, tr_l, 1)
                    logging.info(disp)
                    logging.info(tr_l)
                    logging.info('-' * 20)

                # print(content_cut)
                rw_file(q_path, 'w', tr_con=content_cut)
                logging.info('完成翻译文件:' + q)
                logging.info('-' * 20)
                print('完成翻译文件:' + q)

    # 检查是否同名文件,存在同名则删除,请将翻译完成后的整合包转移到其他地方存放
    # zip_dir(package_path, tr_package + package)
    # print('翻译完成:', package)
