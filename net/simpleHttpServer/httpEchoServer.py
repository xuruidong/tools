#!/usr/bin/env python3
import os,sys,time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import ssl
import argparse

os.path.dirname(__file__)

def get_localtime():
    return time.strftime('%Y-%m-%d %X', time.localtime())


class recvRequestsHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        print ("33333")
        pass   
    
    def do_handle(self):
        print ("Recv http request from %s @%s" %(str(self.client_address),get_localtime()))
        content_length = int(self.headers.get('Content-Length', 0))
        recvData = self.rfile.read(content_length)
        print (recvData)
        self.send_response(200,"Recv POST request success")
        self.send_header("Content-type", "application/json; charset=UTF-8")
        self.end_headers()
        
        headers = {}
        for hd in self.headers:
            headers[hd] = self.headers[hd]
        retDic = {}
        retDic["method"] = self.command
        retDic["path"] = self.path
        retDic["headers"] = headers
        retDic["body"] = recvData.decode()
        retDic["query"] = self.requestline
        self.wfile.write(bytes(json.dumps(retDic), 'utf-8'))
        

    def handle_one_request(self):
        """Handle a single HTTP request.
    
        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.
    
        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            """
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                        HTTPStatus.NOT_IMPLEMENTED,
                        "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            """
            self.do_handle()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return    

    
if __name__ == "__main__":
    args = argparse.ArgumentParser(description = 'argparse Information ',
                                   epilog = 'argparse end ')
    args.add_argument("--ip", "-H", 
                    default = "", help = "set ip, default: 0.0.0.0")
    args.add_argument("--port", "-p",  type = int, 
                    default = 8080, help = "set port, default: 8080")
    args.add_argument("--ssl", "-s",  action='store_true', 
                    help = "enable ssl")
    args = args.parse_args()
    
    print (args)
    print (args.ip)
    print (args.port)
    print (args.ssl)
    
    addr = (args.ip, args.port)
    server = HTTPServer(addr,recvRequestsHandler)
    if args.ssl:
        server.socket = ssl.wrap_socket(server.socket, certfile='cert/test.cert.pem', keyfile='cert/test.key.pem', server_side=True)
    print ("listening at %s ......"%(str(addr)))
    server.serve_forever()
