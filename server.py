#  coding: utf-8
import socketserver
import  datetime
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):


    # does all the work required to service a request.
    def handle(self):

        self.data = self.request.recv(1024).strip()


        if self.data:

            method = self.data.split()[0]
            path = self.data.split()[1]

            URL = os.path.abspath(os.getcwd() + '/www' + path.decode() )


            # Check for Post/Get
            response = self.isGet(method)

            # serve the GET
            if response:


                #print(os.path.exists(URL))

                if( os.path.exists(URL) and "www" in URL):

                        self.serveGet(URL, path)
                else:


                    status_message = "404 Not Found"
                    mime_type = "html"
                    contents = "<html> <head> \r\n" + \
                    "<title>404 Not Found</title> \r\n" + \
                    "</head><body> \r\n" + \
                    "<h1>404 Not Found</h1>\r\n" + \
                    "<p>The Web server cannot find the file or script you asked for. \r\n" + \
                    "</body></html>"
                    self.sendResponse(status_message,contents,mime_type)

            # not GET do not serve
            else:
                return

        # no data
        else:

            return



    # check for get Messages
    # https://www.tutorialspoint.com/http/http_responses.htm

    def isGet(self,method):



        if b"GET" not in method: # 405 Error, Method not supported

            mime_type="text/html"
            status_message = "405 Method Not Allowed"
            contents = "<html> <head> \r\n" + \
            "<title>405 Method Not Allowed</title> \r\n" + \
            "</head><body> \r\n" + \
            "<h1>405 Method Not Allowed</h1>\r\n" + \
            "</body></html>"

            self.sendResponse(status_message, contents, mime_type)

            return False

        else:
            return True




    def sendResponse(self, status_message, contents, mime_type):

        response = "HTTP/1.1 " + status_message + "\r\n" + \
        "Date: " + datetime.datetime.today().strftime("%a, %d %B %Y %X %Z") + "\r\n" \
        "Content-type: text/" + mime_type + "\r\n" + \
        "Content-length: " + str(len(contents)) + "\r\n\r\n" + \
        contents + "\r\n"



        self.request.sendall(str.encode(response))



    def serveGet(self, URL, path):

        status_message = "200 OK"

        #print(path.decode())
        try:
            if ".html" in URL:
                mime_type="html"

            elif ".css" in URL:
                mime_type="css"
            else:
                mime_type="html"

        except IOError:
            pass

        # base url like http://127.0.0.1:8080 add the index.html
        if path.decode()[-1] == '/':
                URL += '/index.html'


        try:
            file_contents = open(URL, 'r').read()

        # The file path exists but it points to a folder, serve 301 error.
        except Exception as e:
            status_message = "301 Moved Permanently"

            response = "HTTP/1.1 " + status_message + "\r\n" + \
            "Date: " + datetime.datetime.today().strftime("%a, %d %B %Y %X %Z") + "\r\n" \
            "Location: " + path.decode() + "/ \r\n" + \
            "Content-type: text/" + mime_type + "\r\n"

            self.request.sendall(str.encode(response))
            return


        self.sendResponse(status_message, file_contents, mime_type)

        return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
