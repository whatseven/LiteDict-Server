import hashlib
import json
import os
import random
import re
import sqlite3
import time

import requests
from flask import Flask, request, Response, abort

from MDXTools.mdict_query import IndexBuilder
from MyHtmlParser import MyHTMLParser
from ext import WORDRECORD, CSSSTATIC, JSSTATIC, JQUERYSTATIC

app=Flask(__name__)

# Add word
@app.route("/add",methods=["GET","POST"])
def AddWord():
    if 'GET'==request.method:
        pass
    elif 'POST'==request.method:
        Word = request.form.get('word')
        Transaction = request.form.get('transaction')
        Description = request.form.get('description')

        cn = sqlite3.connect(WORDRECORD)
        cu = cn.cursor()

        # Find if it is exist
        cu.execute('select proficiency from record where word=?',(Word,))
        res=cu.fetchone()
        if res is None:
            cu.execute("INSERT INTO record (word, wordTransaction, description, insertTime) "
                   "VALUES (?,?,?,?)", (Word, Transaction, Description, time.time()))
        else:
            ProficiencyIncreament=100 if res[0]+25>100 else 100
            cu.execute("update record set proficiency=? where word = ?",(ProficiencyIncreament,Word))
        cn.commit()
        cn.close()

        return 'ok'

# Transaction
@app.route("/transaction",methods=["GET","POST"])
def Transaction():
    if 'GET'==request.method:
        pass
    elif 'POST'==request.method:
        Word=request.form.get("word")
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

        return json.dumps(ResultTransaction)

# Sychronize
@app.route("/sychronize",methods=["GET","POST"])
def Sychronize():
    if 'GET'==request.method:
        LocalTime=request.values.get("LocalTime")
        # Download
        if os.stat(WORDRECORD).st_mtime>=float(LocalTime):
            with open(WORDRECORD, 'rb') as TargetFile:
                data = TargetFile.read()
            response = Response(data, content_type='application/octet-stream')
            response.status_code=200
            return response
        else:
            response = Response()
            response.status_code=302
            return response
    elif 'POST'==request.method:
        try:
            with open(WORDRECORD, 'wb') as TargetFile:
                TargetFile.write(request.data)
            response = Response()
            return response
        except Exception as e:
            abort()

# Remove
@app.route("/remove",methods=["POST"])
def Remove():
    if 'POST'==request.method:
        Word=request.form.get("word")
        # Remove
        cn = sqlite3.connect(WORDRECORD)
        cu = cn.cursor()
        cu.execute('delete from record where word=?',(Word,))
        cn.commit()
        cn.close()

        return 'ok'

if __name__=='__main__':
    app.run(host='0.0.0.0',port=7005)