#!/usr/bin/env python3
import os,sys,time
from http.server import HTTPServer, BaseHTTPRequestHandler


os.path.dirname(__file__)

def get_localtime():
    return time.strftime('%Y-%m-%d %X', time.localtime())

def do_request_process(recvData):
    
    retDic = {"status":"ok"} 
    
    return (retDic)

class recvRequestsHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        print ("33333")
        pass
        
    def do_GET(self):
        print ("Recv http GET request from %s" % str(self.client_address))
        print (self.path)
        self.send_response(200, "recv GET request success")
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()
        index_html = "<!doctype html> \
        <html> \
        <head> \
        <meta charset=\"utf-8\"> \
        <title>Welcome to simpleHttpServer!</title> \
        <style>\
            body {\
                width: 35em;\
                margin: 0 auto;\
                font-family: Tahoma, Verdana, Arial, sans-serif;\
            }\
        </style>\
        </head> \
        <body> \
        <h1>Welcome to simpleHttpServer!</h1>\
        <p>If you see this page, the simple http test server is successfully installed and working. Further configuration is required.</p>\
        <p>Server Time is %s</p> \
        </body> \
        </html>" % (get_localtime())
        self.wfile.write(bytes(index_html, 'utf-8'))
        return index_html    
    
    def do_POST(self):
        print ("Recv http POST request from %s @%s" %(str(self.client_address),get_localtime()))
        print (self.path)
        recvData = self.rfile.read(int(self.headers['Content-Length']))
        print (recvData)
        self.send_response(200,"Recv POST request success")
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()
        retDic = do_request_process(recvData)   
        self.wfile.write(bytes(str(retDic), 'utf-8'))
    

def taskRecvProbeRequests(listen_ip,listen_port):
    addr = (listen_ip,listen_port)
    server = HTTPServer(addr,recvRequestsHandler)
    print ("listening at %s ......"%(str(addr)))
    server.serve_forever()
    return 0


    

    
if __name__ == "__main__":
    
    taskRecvProbeRequests('', 8080)
    