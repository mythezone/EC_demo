import json 

st='{"id":"10.17.29.27:60012","type":"registered","content":{"msg":"success to register","url":"accident.txt","status":"success"}}'
print(st)
j=json.loads(st)
print(j['type'])