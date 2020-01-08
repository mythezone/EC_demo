import socket,json,sys,time,os

class server:
    def __init__(self):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('localhost',6789))
    
    def run(self):
        self.s.listen(10)
        while True:
            conn,addr=self.s.accept()
            print(addr,conn)
            r=conn.recv(1024)
            print(r.decode())
            r2=conn.recv(1024)
            print(r2.decode())
            r3=conn.recv(2048)
            print(r3.decode())
            r3=conn.recv(2048)
            print(r3.decode())

if __name__ == '__main__':
    s=server()
    s.run()
