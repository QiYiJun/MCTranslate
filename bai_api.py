import hashlib
import requests


def sign(appid, y_lang, salt, key):
    sign_ = appid + y_lang + salt + key
    md5_ = hashlib.md5()
    md5_.update(sign_.encode('utf-8'))
    return md5_.hexdigest()


def translate(y_lang):
    # 百度翻译url
    bai_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    # appid,到百度翻译控制台看 https://fanyi-api.baidu.com/api/trans/product/desktop
    appid = '20220904001331072'
    # 密钥,同上
    key = 'qUVeIIVwZiIMYKOO6nlu'
    # 设置salt用于校验MD5值,可自定义,我用自己QQ号
    salt = '1497055242'
    # post请求的表单数据,详情可参考 https://fanyi-api.baidu.com/product/113
    data = {
        "q": y_lang,
        "from": "en",
        "to": "zh",
        "appid": appid,
        "salt": salt,
        "sign": sign(appid, y_lang, salt, key)
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
