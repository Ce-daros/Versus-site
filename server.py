from flask import Flask, request
import time
import csv
import json
app = Flask(__name__)
pks={}
pks_list=[]
pks_json=""
invaild_time=time.time()-10.0
app.config['JSON_AS_ASCII'] = False

def read_pks():
    global pks,pks_json,invaild_time,pks_list
    pks.clear()
    with open('data.csv',encoding="UTF-8") as f:
        for row in csv.reader(f,skipinitialspace=True):
            pks[row[0]]=[row[1],row[2],int(row[3]),int(row[4])]
    pks_json=json.dumps(pks)
    print("Read finish.Readed: " + str(pks))
    dic_to_list()

def dic_to_list():
    global pks,pks_json,invaild_time,pks_list
    pks_list.clear()
    for key,value in pks.items():
        pks_list.append([int(key),value[0],value[1],int(value[2]),int(value[3])])
    print("Read finish.Readed: " + str(pks_list))

def insert_pks(thing1,thing2):
    global pks,pks_json,invaild_time,pks_list
    with open('data.csv','w',encoding="UTF-8",newline='') as f:
        writer = csv.writer(f)
        pks_list.append([str(len(pks)),thing1,thing2,0,0])
        writer.writerows(pks_list)
            
def agree_pks(key,thingname):
    global pks,pks_json,invaild_time,pks_list
    if(pks[key][0]==thingname):
        pks[key][2]=pks[key][2]+1
        
    elif(pks[key][1]==thingname):
        pks[key][3]=pks[key][3]+1
    print(thingname,thingname+"ddd",pks[key][1]==thingname)
    rewrite_pks()

def rewrite_pks():
    global pks,pks_json,invaild_time,pks_list
    with open('data.csv','w',encoding="UTF-8",newline='') as f:
        writer = csv.writer(f)
        dic_to_list()
        writer.writerows(pks_list)

@app.route('/get_pks', methods=['GET'])
def return_pks():
    global pks,pks_json,invaild_time,pks_list
    print("Get request.")
    if(time.time()>invaild_time):
        print("Information is invaild.Reading again...")
        read_pks()
        invaild_time=invaild_time+30
    return pks_json

@app.route('/add_pks',methods=['POST'])
def add_pks():
    global pks,pks_json,invaild_time,pks_list
    print("Request got.")
    r=request.data.decode()
    t1=str.split(r," ")[0]
    t2=str.split(r," ")[1]
    print("Will add: " + t1 + " vs " + t2)
    read_pks()
    insert_pks(t1,t2)
    print("Add finish.Re-read csv...")
    read_pks()
    return 'Success'

@app.route('/agree_pks',methods=['POST'])
def agree_pk():
    global pks,pks_json,invaild_time,pks_list
    print("Request got.")
    r=request.data.decode()
    k=str.split(r," ")[0]
    t=str.split(r," ")[1]
    print("Will agree: " + t + " of " + k)
    read_pks()
    agree_pks(k,t)
    print("Agree finish.Re-read csv...")
    read_pks()
    return 'Success'

if __name__ == '__main__':
    app.run(port=5000, debug=True)