import socket,json
from utils import cprint

if __name__ == '__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("10.17.62.150",11000))
    cprint("Try to send a message:'hello,world'",'yellow')
    msg="Hello,world!".encode()
    js=json.dumps({"type":"hello","content":"world"}).encode()

    s.send(js)
    s.shutdown(1)
    print(js)
    cprint("Try to recv a message from the server:",'yellow')
    r=s.recv(1024)
    print("RECV:",r.decode())
    s.close()
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("10.17.62.150",11000))
    s.send("hello,world!".encode())
    s.shutdown(1)
    r=s.recv(1024)
    

    print("RECV:",r.decode())