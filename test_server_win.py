import time
import urlparse
from pytest import run_local
import BaseHTTPServer


HOST_NAME = '10.0.12.22'  #'192.168.20.1'
PORT_NUMBER = 9000
TEST_LIMITOR = '&'
THREADHOLD = 2

class ReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        test_result_list = []
        fields = self.path[2:].split(TEST_LIMITOR)
        item_fields = []
        for field in fields:
            if '=' in field:
                item_fields.append(field.split('=')[1])
        wf = open("volunteer.txt", 'a')
        for i in item_fields:
            wf.write("{} |".format(i))
        wf.write("\n")
        wf.close()
        counters = {"Animals":0,"Youth_Edu":0,"Environment":0,"Health":0,"Schools":0}
        rf = open("volunteer.txt", 'r')
        for data in rf.readlines():
            print data
            if "Animals" in data:
                counters["Animals"] += 1
            elif "Youth_Edu" in data:
                counters["Youth_Edu"] += 1
            elif "Environment" in data:
                counters["Environment"] += 1
            elif "Health" in data:
                counters["Health"] += 1
            elif "Schools" in data:
                counters["Schools"] += 1
        rf.close()

        print counters
        self.wfile.write("<html><head><title>Volunteer Results</title></head>")
        self.wfile.write("<body><p>Volunteer Results</p>")
        found = False
        for key in counters.keys():
            if counters[key] >= THREADHOLD:
                found = True
                self.wfile.write("<div>{} activity met the expectation with count of {}.  Email will be sent to stake holders</div>".format(key, counters[key]))
        if not found:
            self.wfile.write("<div> All volunteer categories are under expectation</div>")
        self.wfile.write("</body></html>")

    '''
    @staticmethod
    def run_test(test_req):
        test_list = []
        items = test_req.split('=')
        test_list.append(items[1])
        test_results = []
        for item in test_list:
            test_results.append(run_local("python pytest.py --test {}".format(item)))
        return test_results'''


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ReqHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - {}:{}".format(HOST_NAME, PORT_NUMBER)
