import SimpleHTTPServer
import SocketServer


class EnwheelHTTPServer(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    A SimpleHTTPServer.SimpleHTTPRequestHandler subclass that only allows access
    to /simple/*
    """

    def do_GET(self):
        if self.path.startswith('/simple/'):
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.send_response(301)
            self.send_header('Location', '/simple' + self.path)
            self.end_headers()
            return


def serve_command(**kwargs):
    Handler = EnwheelHTTPServer
    port = int(kwargs.get('--port') or '8000')
    httpd = SocketServer.TCPServer(("", port), Handler)

    print 'serving /simple/ on port %s' % port

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            httpd.server_close()
