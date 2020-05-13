#!/usr/bin/env python3

from flask import Flask
from flask import request

app = Flask(__name__)

import random


def gen_threads(nmb,ac):
    if nmb == "on":
        f = open("./threads.txt","r")
        threads = dict()
        threads_raw = f.readlines()
        for t in threads_raw:
            threads[t.split(' ',1)[0]]=t.split(' ',1)[1]
    else:
        threads = dict()
    if ac == "on":
        f1 = open("./ac.txt","r")
        acs = dict()
        ac_raw = f1.readlines()
        for t1 in ac_raw:
            acs[t1.split(' ',1)[0]]=t1.split(' ',1)[1]
    else:
        acs = dict()
    threads.update(acs)
    return threads    


class num_desc(object):
    def __init__(self,no,desc,index):
        self.no = no 
        self.desc = desc
        self.index = index + 1

class passwd_table(object):

    def __init__(self,nmb,ac):
        threads = dict()
        threads = gen_threads(nmb,ac)
        self.table = [[],[],[],[],[],[],[],[],[],[]]
        for key in list(threads.keys()):
            for digit in key:
                if int(digit) in range(0,10):
                    self.table[int(digit)].append(num_desc(key,threads[key],key.index(digit)))

    def query(self,passwd):
        nums = []
        result = []
        out = ""
        for i in range(0,10):
            nums.append(str(i))
        for char in passwd:
            if char in nums:
                q = random.sample(self.table[int(char)],1)[0]
                result.append((passwd.index(char)+1,q))
        for r in result:
            out = out + "<h3>第%d位：%s 第%d位</h3>\n"%(r[0],r[1].desc,r[1].index)
        return out 

@app.route('/', methods=['GET'])
def query_form():
    return '''
            <h3>A加密 ver 0.0.2</h3>
            <form action="/" method="post">
            需要加密的字符串：<p><input name="password"></p>
            <input type="checkbox" name="nmb" value="on" /> 常用串（Easy）
            <input type="checkbox" name="ac" value="on" /> 主站相关（Hard）
            <p><button type="submit">生成</button></p>
            </form>
            '''

@app.route('/', methods=['POST'])
def query():
    passwd = request.form['password']
    try:
        nmb = request.form['nmb']
    except:
        nmb = "off"
    try:
        ac = request.form['ac']
    except:
        ac = "off"

    table = passwd_table(nmb,ac)
    return table.query(passwd)
    # return repr(nmb)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
