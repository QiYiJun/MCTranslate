import json
import os
import re
import shutil
import sys
import time
import zipfile
from bai_api import translate
import logging
from v_config import cfg_


# 读写文件
def rw_file(file_path, model, tr_con=''):
    with open(file_path, model, encoding='utf-8') as f:
        if model == 'r':
            # 读取并返回文件内容
            return f.read()
        elif model == 'w':
            f.write(tr_con)
            f.close()


# 压缩文件
def zip_dir(directory, zipname):
    # 这里是将翻译好的整合包进行压缩,输出路径为tr_package,但没写成功,压缩后压缩包中嵌套多层文件夹
    # 失败的方法,压缩出来的包套了多层文件夹
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                outZipFile.write(filepath, filename)
        outZipFile.close()


# 解压文件
def unzip(zips_path, unzip_path):
    pass


# 检索整合包
def search_packages():
    # 检索的整合包路径
    packages_path = os.listdir('package')
    for package in packages_path:
        if os.path.splitext(package)[1] != '.zip':  # 找出zip后缀的路径
            packages_path.remove(package)
    return packages_path


# 索引版本以及汉化区域
def search_tr_areas(packages_path):
    for package in packages_path:
        zip_files = zipfile.ZipFile('package\\' + package)
        zip_files_path = zip_files.namelist()

        game_version = get_game_version(zip_files, package)

        version_cfg = {}
        try:
            version_cfg = cfg_[game_version]
        except KeyError as e:
            logging.error('未配置cfg的游戏版本:' + str(e))

        get_tr_part(zip_files_path, version_cfg, game_version)
        break


# 获取整合包游戏版本
def get_game_version(zip_files, package):
    try:
        # 获取整合包的游戏版本
        game_version = json.loads(zip_files.open('manifest.json').read())['minecraft']['version']
        # print('整合包', package, '已识别游戏版本:', game_version)
        logging.info('整合包"' + package + '"已识别游戏版本为:' + game_version)
        return game_version
    except Exception as e:
        # print('发生异常:', e)
        logging.error('发生异常:', e)
        sys.exit()


# 获取汉化区域
def get_tr_part(zip_files_path, version_cfg, game_version):
    for i in version_cfg:
        for zip_file_path in zip_files_path:
            if zip_file_path.startswith(version_cfg[i]['path_']):
                version_cfg[i]['value_'] = True
                break
    logging.info(version_cfg)


# # package文件夹,删除非.zip格式以外的文件,请不要在package存放任何与整合包无关的文件夹/文件
# for file in packages:
#     if os.path.splitext(file)[1] != '.zip':
#         shutil.rmtree('package\\' + file)
#
# # 重新检索整合包
# packages = os.listdir('package')
#
# # ftbquests路径
# fq = '\\overrides\\config\\ftbquests'
# # 翻译完成的整合包路径
# tr_package = 'tr_package\\'

# # 解压整合包
# for package in packages:
#     # 获取整合包的名字,后续用作解压路径
#     package_path = 'package\\' + os.path.splitext(package)[0]
#     # 整合包对应的ftbquests路径
#     fq_path = package_path + fq
#     # 解压整合包至相应文件夹
#     with zipfile.ZipFile('package\\' + package) as unzip:
#         unzip.extractall(package_path)
#         unzip.close()
#
#     # # 如果存在ftbquests文件,则进行文件检索并翻译
#     if os.path.exists(fq_path):
#         for i in os.listdir(fq_path):
#             quests_file_path = fq_path + '\\' + i + '\\chapters\\'
#             # 检索ftbquests文件路径
#             files_name = os.listdir(quests_file_path)
#             # ftbquests的文件翻译
#             for q in files_name:
#                 logging.info('开始翻译文件:' + q)
#                 logging.info('-' * 20)
#                 print('开始翻译文件:' + q)
#
#                 q_path = quests_file_path + q
#                 content = rw_file(q_path, 'r')
#                 # print(content)
#
#                 # 正则 消除MC的格式化代码样式
#                 # 详情参考 https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81
#                 content_cut = re.sub('&\w', '', content)
#                 # 正则 寻找title和subtitle中的翻译内容
#                 title_langs = re.findall('[sub]*title: \"(.*)\"', content_cut)
#                 # print(title_langs)
#
#                 # 翻译内容并覆写原文件
#                 for title in title_langs:
#                     tr_l = translate(title)
#                     content_cut = content_cut.replace(title, tr_l, 1)
#                     logging.info(title)
#                     logging.info(tr_l)
#                     logging.info('-' * 20)
#
#                 disp_all = re.findall('\tdescription: \[([\s\S]*?)]', content_cut)
#                 disp_langs = []
#                 for d in disp_all:
#                     disp_s = re.findall('\"(.*)\"', d)
#                     for di in disp_s:
#                         if di != '' and len(re.findall('width|height|align', di)) != 3:
#                             disp_langs.append(di)
#
#                 for disp in disp_langs:
#                     tr_l = translate(disp).replace('\\', '')
#                     content_cut = content_cut.replace(disp, tr_l, 1)
#                     logging.info(disp)
#                     logging.info(tr_l)
#                     logging.info('-' * 20)
#
#                 # print(content_cut)
#                 rw_file(q_path, 'w', tr_con=content_cut)
#                 logging.info('完成翻译文件:' + q)
#                 logging.info('-' * 20)
#                 print('完成翻译文件:' + q)

# 由于压缩函数没有写成功,所以翻译好的整合包需要手动打包并安装
# 如果先前已经安装过整合包,替换翻译完成后的文件会是更快的选择

if __name__ == '__main__':
    # 日志配置,保存日志trLog.log
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s]:%(message)s',
                        datefmt='%Y%m%d-%H:%M:%S')
    # 整合包检索
    search_tr_areas(search_packages())
