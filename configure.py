#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import time
import re
import requests
import os
import getpass

currentdir = os.path.dirname(os.path.abspath(__file__))

def AskInteractive(description, options, delta=0):
    print(description)
    for index in range(len(options)):
        print(str(index)+". "+options[index])
    while True:
        ret = input("你的选择: ")
        try:
            val = int(ret)
            if val >= 0 and val < len(options):
                return val+delta
        except:
            pass
    
def AskText(description):
    return input(description)
def Askpassword(description):
    return getpass.getpass(description)
def AskBoolean(description):
    while True:
        ret = input(description+'<Y/N> ').upper()
        if ret == "Y":
            return 1
        elif ret == "N":
            return 0
def location(description):
    north = '{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.23254,"R":108.91514000000001,"lng":108.91514,"lat":34.23254},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"白沙路","streetNumber":"付8号","country":"中国","province":"陕西省","city":"西安市","district":"雁塔区","township":"电子城街道"},"formattedAddress":"陕西省西安市雁塔区电子城街道西安电子科技大学北校区","roads":[],"crosses":[],"pois":[]}'
    south = '{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.122061903212,"R":108.83052978515701,"lng":108.83053,"lat":34.122062},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"264号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[]}'
    while True:
        ret = input(description).upper()
        if ret == "S":
            return south
        elif ret == "N":
            return north
# Configuration

# 具体填报项目

print("#####\n温馨提示： 不外出、不聚集、不吃野味， 戴口罩、勤洗手、咳嗽有礼，开窗通风，发热就诊\n#####\n\n")

data = {}

# 统一认证账号密码
data.update({"_u":AskText("统一认证账号: ")})
data.update({"_p":Askpassword("统一认证密码: ")})

# 今日是否在校
data.update({"sfzx":AskBoolean("今日是否在校: "),"fxyy":""})

# 返校原因
if data["sfzx"] == 1:
    data.update({"fxyy":AskText("返校原因: ")})
    
# 所在地点
IsInChina = AskBoolean("是否在国内: ")
if IsInChina == 0:
    data.update({"area":"国外","city":"国外","province":"国外"})
else:
    # 定位
    data.update({"geo_api_info":location("南校区填S，北校区填N：")})
    geo = json.loads(data["geo_api_info"])
    data.update({"address":geo["formattedAddress"],"area":geo["addressComponent"]["province"] + ' ' + geo["addressComponent"]["city"] + ' ' + geo["addressComponent"]["district"],"province":geo["addressComponent"]["province"],"city":geo["addressComponent"]["city"]})
    if data["city"].strip() == "" and data["province"] in ["北京市","上海市","重庆市","天津市"]:
        data["city"] = data["province"]
    
# 当前地点与上次不在同一城市
data.update({"ismoved":AskBoolean("当前地点与上次是否不在同一城市: "),"bztcyy":""})
if data["ismoved"] == 1:
    data.update({"bztcyy":AskInteractive("当前地点与上次不在同一城市,原因如下: ",["其他","探亲","旅游","回家"])})

# 今日是否在中高风险地区
data.update({"zgfxdq":AskBoolean("今日是否在中高风险地区：")})

# 体温范围
data.update({"tw":AskInteractive("今日体温范围(℃): ",["(-inf, 36]","(36, 36.5]","(36.5, 36.9]","(36.9, 37.3]","(37.3, 38]","(38, 38.5]","(38.5, 39]","(39, 40]","(40, +inf)"],1)})

# 今日是否到过或者经停武汉
#data.update({"sftjwh":AskBoolean("今日是否到过或者经停武汉: ")})

# 今日是否到过或者经停湖北其他地区(除武汉)
#data.update({"sftjhb":AskBoolean("今日是否到过或者经停湖北其他地区(除武汉): ")})

# 今日是否出现发热、乏力、干咳、呼吸困难等症状
data.update({"sfcxtz":AskBoolean("今日是否出现发热、乏力、干咳、呼吸困难等症状: "),"sfyyjc":0,"jcjgqr":0,"jcjg":""})

# 是否到相关医院或门诊检查
if data["sfcxtz"] == 1:
    data.update({"sfyyjc":AskBoolean("是否到相关医院或门诊检查: ")})
    
# 检查结果属于以下哪种情况
if data["sfyyjc"] == 1:
    data.update({"jcjgqr":AskInteractive("检查结果属于以下哪种情况: ",["疑似感染","确诊感染","其他"],1)})
    
# 诊疗情况
if data["jcjgqr"] in [1, 2, 3]:
    data.update({"jcjg":AskText("诊疗情况: ")})
    
# 今日是否与武汉市或武汉周边的人员有过较为密集的接触
#data.update({"sfjcwhry":AskBoolean("今日是否与武汉市或武汉周边的人员有过较为密集的接触: ")})

# 今日是否与湖北其他地区(除武汉外)的人员有过较为密集的接触
#data.update({"sfjchbry":AskBoolean("今日是否与湖北其他地区(除武汉外)的人员有过较为密集的接触: ")})

# 今日是否接触无症状感染/疑似/确诊人群
data.update({"sfjcbh":AskBoolean("今日是否接触无症状感染/疑似/确诊人群: "),"jcbhlx":"","jcbhrq":""})

if data["sfjcbh"] == 1:
    # 接触人群类型
    touch_list=["疑似","确诊"]
    date.update({"jcbhlx":touch_list[AskInteractive("接触人群类型: ",touch_list)]})
    # 接触日期
    date.update({"jcbhrq":AskText("接触日期(YYYY-MM-DD): ")})

# 今日是否接触密接人员
data.update({"mjry":AskBoolean("今日是否接触密切接触人员: ")})

# 近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触
data.update({"csmjry":AskBoolean("近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触: ")})

# 今日是否接触境外人员
data.update({"sfjcjwry":AskBoolean("今日是否接触境外人员: ")})

# 是否处于隔离期
data.update({"sfcyglq":AskBoolean("是否处于隔离期: "),"gllx":"","glksrq":""})


if data["sfcyglq"] == 1:
    # 隔离场所
    iso_list=["校内居家隔离","校内医院隔离","校外居家隔离","校外西安市内医学隔离","校外西安市内集中隔离","西安市外地区医学隔离"]
    date.update({"gllx":iso_list[AskInteractive("隔离场所: ",iso_list)]})
    # 隔离开始日期
    date.update({"glksrq":AskText("隔离开始日期(YYYY-MM-DD): ")})
    
# 是否有任何与疫情相关的,值得注意的情况
data.update({"sfcxzysx":AskBoolean("是否有任何与疫情相关的,值得注意的情况: "),"qksm":""})

# 情况说明
if data["sfcxzysx"] == 1:
    data.update({"qksm":AskText("情况说明: ")})
    
# 其他信息
data.update({"remark":AskText("其他信息: ")})

with open(currentdir + "/data.json","w") as fd:
    json.dump(data,fd)
    print("数据保存成功")


#############################################################


data = {}

# 是否开启server_chan
data.update({"server_chan":AskBoolean("是否开启server_chan: ")})

# 开启server_chan
if data["server_chan"] == 1:
    data.update({"key_server":AskText("请输入密匙: ")})

# 设置socks
proxies = {}


# 是否开启telegram_bot
data.update({"telegram_bot":AskBoolean("是否开启telegram_bot: ")})
# 开启telegram_bot
if data["telegram_bot"] == 1:
    data.update({"key_bot":AskText("请输入密匙: ")})
    data.update({"open_proxy":AskBoolean("是否开启代理登录: ")})
    if data["open_proxy"] == 1:
        proxies.update({"http":"socks5://" + input("http代理:\n输入ip:") + ":" + input("输入端口：")})
        proxies.update({"https":"socks5://" + input("https代理:\n输入ip:") + ":" + input("输入端口：")})
    # 获取chat id
    url = "https://api.telegram.org/bot" + \
        data['key_bot'] + \
            "/getUpdates"
    id = json.loads((re.search('"chat":({.*}),"date"', requests.session().get(url, proxies = proxies).text).group(1)))
    data.update({"chat_id":id['id']})


with open(currentdir + "/notice.json","w") as fd:
    json.dump(data,fd)
    print("提醒服务保存成功")

with open(currentdir + "/proxies.json","w") as fd:
    json.dump(proxies,fd)
    print("代理保存成功")

time.sleep(10)
