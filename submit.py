#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import json
import requests
import re
import sys
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header

currentdir = os.path.dirname(os.path.abspath(__file__))


def time_judge(offset=0):
    t = int(time.strftime("%H", time.localtime())) + offset
    if t < 8:
        return "凌晨\n"
    elif t < 12:
        return "早上\n"
    elif t < 14:
        return "中午\n"
    elif t < 18:
        return "下午\n"
    elif t < 24:
        return "晚上\n"
    else:
        print("时间错误")
        exit(1)


def ReBoolean(x):
        if x == 1:
            return "是"
        elif x == 0:
            return '否'


def ReTiWen(x):
    list_tw = ["(-inf, 36]","(36, 36.5]","(36.5, 36.9]","(36.9, 37.3]","(37.3, 38]",\
        "(38, 38.5]","(38.5, 39]","(39, 40]","(40, +inf)"]
    return list_tw[x-1]


def mail_notice(dict_, dict_switch):

    if dict_switch['m'] == "执行完毕！":
        message = MIMEText(dict_['text'], 'plain', 'utf-8')
        message['From'] = Header("签到服务", 'utf-8')   # 发送者
        
        
        message['Subject'] = Header(dict_['subject'], 'utf-8')
        
        content = ssl.create_default_context()
        try:
            smtpObj = smtplib.SMTP(dict_['mail_host'], dict_['mail_port'])
            smtpObj.set_debuglevel(1)
            smtpObj.ehlo()
            smtpObj.starttls(context=content)
            smtpObj.ehlo()
            smtpObj.login(dict_['mail_user'], dict_['mail_pass'])
            smtpObj.sendmail(dict_['sender'], dict_['receivers'], message.as_string())
            smtpObj.close()
            print ("邮件发送成功!")
        except smtplib.SMTPException:
            print ("Error: 无法发送邮件!")
    elif dict_switch['m'] == "今天已经填报了":
        print("已经发送过邮件了!\n")
    else:
        print("其他错误发生！")


def notice_func(predef, input, offset=0):
    input = json.loads(input.text)
    conn = requests.Session()
    content = { "sfzx":"今日是否在校:", "address": "所在地点：", "zgfxdq":"今日是否在中高风险地区：", \
        "tw":"今日体温范围(℃): ", "sfcxtz":"今日是否出现发热、乏力、干咳、呼吸困难等症状: ", \
            "sfjcbh":"今日是否接触无症状感染/疑似/确诊人群: ", "mjry":"今日是否接触密切接触人员: ", \
                "csmjry":"近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触: ", \
                    "sfcyglq":"是否处于隔离期:", "sfjcjwry":"今日是否接触境外人员: ", "sfcxzysx":"是否有任何与疫情相关的,值得注意的情况: ", \
                        "remark":"其他信息: " }
    text = f"{time.strftime('具体时间：%Y-%m-%d', time.localtime())} {str(int(time.strftime('%H', time.localtime()))+offset)}:{time.strftime('%M:%S', time.localtime())}\n\
    {content['sfzx']}{ReBoolean(predef['sfzx'])}\n\
    {content['address']}{predef['address']}\n\
    {content['zgfxdq']}{ReBoolean(predef['zgfxdq'])}\n\
    {content['tw']}{ReTiWen(predef['tw'])}\n\
    {content['sfcxtz']}{ReBoolean(predef['sfcxtz'])}\n\
    {content['sfjcbh']}{ReBoolean(predef['sfjcbh'])}\n\
    {content['mjry']}{ReBoolean(predef['mjry'])}\n\
    {content['csmjry']}{ReBoolean(predef['csmjry'])}\n\
    {content['sfcyglq']}{ReBoolean(predef['sfcyglq'])}\n\
    {content['sfjcjwry']}{ReBoolean(predef['sfjcjwry'])}\n\
    {content['sfcxzysx']}{ReBoolean(predef['sfcxzysx'])}\n\
    {content['remark']}{predef['remark']}\n\
    {input['m']}\n"

    print_output_log(text)
    
    if not os.path.exists(currentdir + "/notice.json"):
        exit(0)
    with open(currentdir + "/notice.json", "r") as fd:
        data1 = json.load(fd)

    if data1['server_chan'] == 1:
        url = "http://sc.ftqq.com/" +\
             data1['key_server'] + \
                 ".send"
        data = {'text':'疫情通填报报告：' + time_judge(offset), 'desp':f'{text}'}
        conn.post(url, data = data)


    if data1['telegram_bot'] == 1:
        url = "https://api.telegram.org/bot" + \
            data1['key_bot'] + \
                "/sendMessage"
        data = {'chat_id':data1['chat_id'], 'text':f'疫情通填报报告：\n时间：{time_judge(offset)}{text}'}
        # 读取代理设置
        if  os.path.exists(currentdir + "/proxies.json"):
            with open(currentdir + "/proxies.json", "r") as fd:
                proxies = json.load(fd)        
            conn.post(url, data = data, proxies = proxies)
        else:
            conn.post(url, data = data)

    email = {'receivers':'', 'text':f'疫情通填报报告：\n时间：{time_judge(offset)}{text}', 'mail_host':'', 'mail_user':'', 'mail_pass':'', 'mail_port':, \
            'sender':'', 'subject':f'疫情通填报报告：{time_judge(offset)}'}
    mail_notice(email, input)


def print_output_log(text):
    print("正在记录日志中......\n")
    output_str = "最终输出：\n"
    output_str += text
    print(output_str)
    with open(currentdir + "/output.log", "a") as fd:
        fd.write(output_str)


def submit():
    if os.path.exists("NOSUBMIT"):
        exit()

    data = {}

    with open(currentdir + "/data.json") as fd:
        data=json.load(fd)
        
    conn = requests.Session()

    # Login
    result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',data={'username':data['_u'],'password':data['_p']})
    if result.status_code != 200:
        print('认证大失败')
        exit()

    # Submit
    result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
    if result.status_code != 200:
        print('获取页面大失败')
        exit()

    predef = json.loads(re.search('var def = ({.*});',result.text).group(1))

    if "dump_geo" in sys.argv:
        print(predef['geo_api_info'])
        exit()

    try:
        del predef['jrdqtlqk']
        del predef['jrdqjcqk']
    except:
        pass
    del data['_u']
    del data['_p']

    predef.update(data)

    result = conn.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save',data=predef)
    return predef, result


if __name__ == "__main__":
    predef, result = submit()
    notice_func(predef, result, offset=0)
    print("执行完毕！")
