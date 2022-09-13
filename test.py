# -*- coding: UTF-8 -*-
import zipfile

archive = zipfile.ZipFile('package\\Age+of+Fate+v1.5.5.zip')

for file in archive.namelist():
    # print(file)
    if file.startswith('overrides/config/ftbquests'):
        print('检测到FTB任务')
        break
