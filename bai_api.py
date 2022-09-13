import hashlib
import json

import requests


def sign(appid, y_lang, salt, key):
    sign_ = appid + y_lang + salt + key
    md5_ = hashlib.md5()
    md5_.update(sign_.encode('utf-8'))
    return md5_.hexdigest()


def translate(y_lang):
    # 百度翻译url
    bai_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    # 请到 user_cfg.json 文件修改自己的 appid,key,salt
    # appid 可在百度翻译控制台找到 https://fanyi-api.baidu.com/api/trans/product/desktop
    # key 密钥,同上
    # salt 用于校验MD5值,可自定义,我用自己QQ号
    with open('user_cfg.json', 'r', encoding='utf-8') as f:
        user_cfg = json.loads(f.read())
        f.close()

    # post请求的表单数据,详情可参考 https://fanyi-api.baidu.com/product/113
    data = {
        "q": y_lang,
        "from": "en",
        "to": "zh",
        "appid": user_cfg.appid,
        "salt": user_cfg.salt,
        "sign": sign(user_cfg.appid, y_lang, user_cfg.salt, user_cfg.key)
    }
    # 请求头,非必要时不要修改
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70"
    }

    res = requests.post(url=bai_url, headers=header, data=data).json()
    try:
        return res['trans_result'][0]['dst']
    except KeyError:
        print(res)
        print('q:', y_lang)
