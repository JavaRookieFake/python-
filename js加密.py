# 反爬手段 
# 1：限制请求的频次 【延时请求、ip代理】
# 请求头  【模拟真实的浏览器请求】
# 返回数据 加密
# 字体加密 css加密
# cookie 加密
# 验证码 【滑动、倒立文字，图文混排】
# js 混淆加密

import requests
import time
import hashlib #加密的库
import json
from urllib import parse

def getSalt():
    '''
    salt的公式r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
    把它翻译成python代码
    '''
    import time, random

    salt = int(time.time()*1000) + random.randint(0, 10)

    return salt

def getMD5(parms):
    '''
    md5加密
    :param parms: 被加密的参数数据
    :return:
    '''
    md5 = hashlib.md5()
    md5.update(parms.encode('utf-8'))
    sign = md5.hexdigest()

    return sign

def getSign(key, salt):
    '''
    模拟js的加密过程
    :param key:
    :param salt:
    :return: md5加密后的数据
    '''
    sign = "fanyideskweb" + key + str(salt) + "n%A-rKaT5fb[Gy?;N5@Tj"
    sign = getMD5(sign)
    return sign

def youdao(key):
    # url从http://fanyi.youdao.com输入词汇 抓包得到
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=true"
    # t= n.md5(navigator.appVersion)
    # , r = "" + (new Date).getTime()
    # , i = r + parseInt(10 * Math.random(), 10);
    salt = getSalt()
    # data从右键检查FormData得到 并分析加密过程
#     i: name
# from: AUTO
# to: AUTO
# smartresult: dict
# client: fanyideskweb
# salt: 15713891081420
# sign: e0630feba90d5d4e4b54c2ebf40e0311
# ts: 1571389108142
# bv: 530358e1f56d925c582f7d2d49f07756
# doctype: json
# version: 2.1
# keyfrom: fanyi.web
# action: FY_BY_REALTlME
    data = {
        "i": key,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": str(salt),
        "sign": getSign(key, salt),
        "doctype": "json",
        'ts':int(time.time()*1000),
        'bv':getMD5('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'),
        "version": "2.1",
        "keyform": "fanyi.web",
        "action": "FY_BY_REALTIME",

    }
    # print(data)
    # 对data进行编码，因为参数data需要bytes格式
    data = parse.urlencode(data).encode()
    # headers从右键检查Request Headers得到
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": '{}'.format(len(data)),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/?keyfrom=dict2.top",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    req = requests.post(url=url, data=data, headers=headers)
    rs = json.loads(req.text)
    print(rs)
    print('翻译后的结果是:【%s】'%(rs['translateResult'][0][0]['tgt']))

if __name__ == '__main__':
    youdao(input('请输入要翻译的单词'))
