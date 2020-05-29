from gevent import monkey
monkey.patch_all()

from backend.server import app
