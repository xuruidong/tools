#!/usr/bin/env python3
import os,sys,time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

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
    

class httpStreamServer(recvRequestsHandler):
    def do_handle(self):
        print ("Recv http request from %s @%s" %(str(self.client_address),get_localtime()))
        content_length = int(self.headers.get('Content-Length', 0))
        recvData = self.rfile.read(content_length)
        print (recvData)
        self.send_response(200,"Recv POST request success")
        self.send_header("Content-type", "text/event-stream; charset=UTF-8")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Connection", "keep-alive")
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
        byte_data = bytes(json.dumps(retDic), 'utf-8')
        data_len = len(byte_data)
        
        print(data_len.to_bytes(2, "little") + b"\r\n" + byte_data + b"\r\n")
        # chunk_size = hex(len(byte_data))[2:].encode() + b"\r\n"
        # chunk = chunk_size + byte_data + b"\r\n"
        
        byte_data = "@@@@@@@@@@@@@@@@@\n"
        chunk_size = hex(len(byte_data))[2:] + "\r\n"
        chunk = chunk_size + byte_data + "\r\n"        
                
        for i in range(10):
            #self.wfile.write(data_len.to_bytes(1, "little") + b"\r\n" + byte_data + b"\r\n")
            self.wfile.write(chunk.encode())
            time.sleep(1)
            
        self.wfile.write(b"0\r\n\r\n")
        
    
def taskRecvProbeRequests(listen_ip,listen_port):
    addr = (listen_ip,listen_port)
    server = HTTPServer(addr, httpStreamServer)
    print ("listening at %s ......"%(str(addr)))
    server.serve_forever()
    return 0


    

    
if __name__ == "__main__":
    
    taskRecvProbeRequests('', 8080)
    