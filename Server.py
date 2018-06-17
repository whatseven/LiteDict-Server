import hashlib
import json
import random
import re
from html.parser import HTMLParser

import requests
from flask import Flask, request

from MDXTools.mdict_query import IndexBuilder

app=Flask(__name__)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.data = ''

    def handle_starttag(self, tag, attrs):
        """
        recognize start tag, like <div>
        :param tag:
        :param attrs:
        :return:
        """
        # print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        """
        recognize end tag, like </div>
        :param tag:
        :return:
        """
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        """
        recognize data, html content string
        :param data:
        :return:text
        """
        if '•' in data:
            if not re.search(r"[a-zA-Z]", data):
                if not len(data)<4:
                    self.data += data + '\n'

    def handle_startendtag(self, tag, attrs):
        """
        recognize tag that without endtag, like <img />
        :param tag:
        :param attrs:
        :return:
        """
        # print("Encountered startendtag :", tag)

    def handle_comment(self, data):
        """

        :param data:
        :return:
        """
        # print("Encountered comment :", data)

# Add word
@app.route("/add",methods=["GET","POST"])
def AddWord():
    if 'GET'==request.method:
        pass
    elif 'POST'==request.method:
        Word = request.form.get('word')
        Transaction = request.form.get('transaction')
        Description = request.form.get('description')


        return 'ok'

    # Transaction
@app.route("/transaction",methods=["GET","POST"])
def Transaction():
    if 'GET'==request.method:
        pass
    elif 'POST'==request.method:
        Word = request.form.get('word')
        # Dict Parser
        builder = IndexBuilder('MDXData/niujin.mdx')
        ResultWord = builder.mdx_lookup(Word)
        ResultTransaction=""
        if len(ResultWord) == 0:
            # # YouDao
            # appKey = '4fd37dd83c3b4a86'
            # secretKey = '0euicKCl8dubyDXbvwbgYDMF3Rt6TWGf'
            # q = Word
            # fromLang = 'EN'
            # toLang = 'zh-CHS'
            # salt = random.randint(1, 65536)
            # sign = appKey + q + str(salt) + secretKey
            # m1 = hashlib.md5()
            # m1.update(sign.encode())
            # sign = m1.hexdigest()
            # r = requests.post("http://openapi.youdao.com/api"
            #                   , data={"appKey": appKey
            #         , "q": q
            #         , "from": fromLang
            #         , "to": toLang
            #         , "salt": salt
            #         , "sign": sign})
            # result = json.loads(r.text)
            # ResultTransaction = "From YouDao\n" + result["translation"][0]

            # Baidu
            appKey = '20180418000147886'
            secretKey = '8tuKIpNnEoAOzrr8mrPn'
            q = Word
            fromLang = 'en'
            toLang = 'zh'
            salt = random.randint(32768, 65536)
            sign = appKey + q + str(salt) + secretKey
            m1 = hashlib.md5()
            m1.update(sign.encode())
            sign = m1.hexdigest()
            r = requests.post("http://api.fanyi.baidu.com/api/trans/vip/translate"
                              , data={"appid": appKey
                    , "q": q
                    , "from": fromLang
                    , "to": toLang
                    , "salt": salt
                    , "sign": sign})
            result = json.loads(r.text)
            ResultTransaction = "From BaiDu\n" + result["trans_result"][0]['dst']
        else:
            parser = MyHTMLParser()
            parser.feed(ResultWord[0])
            ResultTransaction = parser.data

        return json.dumps(ResultTransaction)

if __name__=='__main__':
    app.run(host='0.0.0.0')