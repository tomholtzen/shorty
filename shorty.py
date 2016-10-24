import base64
import cherrypy
import random
import threading

url_db = {}
dblock = threading.RLock()

class Shorty(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, find_key=None):
        if not find_key:
            dblock.acquire()
            dump_db = str(url_db)
            dblock.release()
            return dump_db
        else:
            dblock.acquire()
            url = url_db.get(find_key)
            dblock.release()
            if url:
                return {'url': url}
            else:
                raise cherrypy.HTTPError(404)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        encode_me = cherrypy.request.json
        random_num = random.randint(1, 2**32)
        key = base64.b64encode(str(random_num))

        dblock.acquire()
        url_db[key] = encode_me['url']
        dblock.release()

        shortened = "http://localhost:8080/" + key
        return {"key": key, "shortened_url": shortened}

    def DELETE(self, delete_key):
        try:
            dblock.acquire()
            del url_db[delete_key]
        except Exception as e:
            cherrypy.log("key %s not found in url_db" % delete_key)
            raise cherrypy.HTTPError(404);
        finally:
            dblock.release()


class Redirect():
    exposed = True

    def GET(self, url_key):
        dblock.acquire()
        longurl = url_db.get(url_key)
        dblock.release()

        if longurl:
            raise cherrypy.HTTPRedirect(longurl)
        else:
            raise cherrypy.HTTPError(404);


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})

    cherrypy.tree.mount(Redirect(), '/', conf)
    cherrypy.tree.mount(Shorty(), '/api/v1', conf)

    cherrypy.engine.start()
    cherrypy.engine.block()

