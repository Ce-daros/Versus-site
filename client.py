import requests
#r = requests.get("http://127.0.0.1:5000/get_pks")
#print(r.text)
a=input("input key")
b=input("input thing")
r_header = {'key':str(a),'thing':str(b)}
r=requests.post("http://127.0.0.1:5000/agree_pks",data=r_header)
print(r.text)