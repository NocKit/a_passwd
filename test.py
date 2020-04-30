#!/usr/bin/env python3

from flask import Flask
from flask import request

app = Flask(__name__)

import random


def gen_threads():
    f = open("./threads.txt","r")
    threads = dict()
    threads_raw = f.readlines()
    for t in threads_raw:
        threads[t.split()[0]]=t.split()[1]
    return threads    
    

class num_desc(object):
    def __init__(self,no,desc,index):
        self.no = no 
        self.desc = desc
        self.index = index + 1

class passwd_table(object):

    def __init__(self):
        threads = dict()
        threads = gen_threads()
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
            out = out + "<h3>第%d位：%s 串号第%d位</h3>\n"%(r[0],r[1].desc,r[1].index)
        return out 

@app.route('/', methods=['GET'])
def query_form():
    return '''
              <h3>A密码生成器 ver 0.0.1</h3>
              <form action="/" method="post">
              <p><input name="password"></p>
              <p><button type="submit">生成</button></p>
              </form>
            '''

@app.route('/', methods=['POST'])
def query():
    passwd = request.form['password']
    table = passwd_table()
    return table.query(passwd)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
