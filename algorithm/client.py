import sys,os,time,socket,json

def get_json_data(filepath):
    with open(filepath,'r') as f:
        d=json.loads(f.read())
    return d


class client:
    def __init__(self):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def connect(self):
        self.s.connect(('localhost',6789))
        
        self.s.send("hello".encode())
        time.sleep(3)
        self.s.send("world".encode())
        d=get_json_data('accident.json')
        db=json.dumps(d).encode()
        self.s.send(db)

if __name__ == '__main__':
    c=client()
    c.connect()
