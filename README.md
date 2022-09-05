# MC Translate -- 我的世界翻译

## 项目起源

对于翻译整合包的作者们来说, 一个整合包不热门, 作者们很难有动力去进行翻译,光靠爱发电是不够的

对于整合包而言, 玩家们无法或难以理解部分的大多为任务,指南书......等

因此为了改善玩家的游戏体验, 同时也为了能够稍微减轻翻译整合包的作者大大们的工作量

本项目就由此而生, 由于本人的代码能力, 不能将代码写得优雅,非常抱歉

本项目采用百度翻译API, 每月免费100万字符 (高级版, 实名认证)

更多关于翻译API接入部分的详细说明, 请看: [翻译API接入](#翻译API接入)

注:本项目没有任何赞助或商业推广, 因为免费, 所以选择百度翻译. 必应翻译需要借记卡/信用卡

(●'?'●) 记得点 Star ☆ 哦!

## 项目功能

### 目前实现功能

- FTB Quests(FTB任务) 翻译内容包含: 标题, 副标题, 任务描述
    - 已知缺陷:
        - [```格式化代码```](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81)会被清除
        - 当前仅支持```大于 1.12.2 游戏版本```的 FTBQ

### 待实现功能

- Better Quests(更好的任务) 翻译
- Triumph(自定义进度) 翻译
- FTB Guides(FTB指南) 翻译
- Guide Api(指南) 翻译

## 翻译API接入

前面提到本项目默认采用百度翻译API, 首次使用请打开```bai_api.py```文件, 找到函数```translate```填写里面百度翻译需要的相关参数

```
appid | APPID 可在百度云控制台找到
key | 密钥 可在百度云控制台找到
salt | 自定义校验字符串,可为英文数字,长度限制不清楚,个人建议16字符内
```

如果你有自己的翻译API, 请严格按照以下方式接入

你需要创建一个新的py文件, 命名建议:

```
有道翻译 -> youdao_api.py
必应翻译 -> bing_api.py
XX翻译 -> custom_api.py
```

你需要在新建的py文件中写入一个必要的函数```translate```

以及一个必要传递参数```y_lang```(参数名字可自拟, ```y_lang```是待翻译内容, 类型为字符串)

函数的返回值是```翻译后的```内容```retuen tr_lang``` ```tr_lang```可自拟, 但必须是字符串

```
def translate(y_lang) {
    ......
    return tr_lang
}
```

在```main.py```中, 你只需要修改```from bai_api import translate```, 将```bai_api```修改成你新建的py文件名字即可.
例如: ```from custom_api import translate``` 如果你知道其原理, 你可以不遵循上述规定的函数名称

## FAQ

较多的重复的 FAQ 将会在此处列出, 方便大家查找并获得解决方法,
如果没有请提交 [Issues](https://github.com/QiYiJun/MCTranslate/issues)