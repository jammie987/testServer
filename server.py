import tornado.ioloop
import tornado.web
import math
import os
import platform
from tornado import gen
from tornado.concurrent import Future


@gen.coroutine
def get_prime(n):
    """
    Sieve of Eratosthenes
    """
    n = int(n) + 1
    sieve = [True] * n
    for i in range(2, int(math.sqrt(n))):
        for j in range(i * 2, n, i):
            sieve[j] = False
    result = [i for i in range(2, n) if sieve[i]]
    r = ', '.join(str(v) for v in result)
    raise gen.Return(r)


@gen.coroutine
def fact(n):
    '''
    Factorization as dividing by a primes successively
    '''
    result = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            result.append(i)
            n //= i
        else:
            i += 1
    if n > 1:
        result.append(n)
    r = ', '.join(str(v) for v in result)
    raise gen.Return(r)


@gen.coroutine
def ping():
    '''
    Pinging google.com
    '''
    host = "google.com"
    '''Compiling command for OS command line'''
    if platform.system().lower() == "windows":
        ping_str = "-n 1"
    else:
        ping_str = "-c 1"
    r = str(os.system("ping " + ping_str + " " + host) == 0)
    raise gen.Return(r)


@gen.coroutine
def pi(n):
    """
    Calculate n iterations of Archimedes PI recurrence relation
    """
    edge = 2.0
    sides = 4
    for i in range(n):
        edge = 2 - 2 * math.sqrt(1 - edge / 4)
        sides *= 2
    r = str(sides * math.sqrt(edge) / 2)
    raise gen.Return(r)


class PrimeHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, n):
        response = yield get_prime(n)
        self.write(response)


class FactHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, n):
        response = yield fact(int(n))
        self.write(response)


class PingHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        response = yield ping()
        self.write(response)


class PiHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, n):
        response = yield pi(int(n))
        self.write(response)


def make_app():
    return tornado.web.Application([
        (r"/prime/([^/]+)", PrimeHandler),
        (r"/fact/([^/]+)", FactHandler),
        (r"/ping/", PingHandler),
        (r"/pi/([^/]+)", PiHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
