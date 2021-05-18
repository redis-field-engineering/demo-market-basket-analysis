from flask import Flask, render_template, request, redirect, session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_session import Session

import redis
from os import environ
import redisai



# From our local file
#from datasetup import setup_data

if environ.get('REDIS_SERVER') is not None:
   redis_server = environ.get('REDIS_SERVER')
else:
   redis_server = 'localhost'

if environ.get('REDIS_PORT') is not None:
   redis_port = int(environ.get('REDIS_PORT'))
else:
   redis_port = 6379

if environ.get('REDIS_PASSWORD') is not None:
   redis_password = environ.get('REDIS_PASSWORD')
else:
   redis_password = ''

# Setup Connections
conn = redisai.Client(
        host=redis_server,
        port=redis_port,
        password=redis_password
)
rdb = redis.Redis(
        host=redis_server,
        port=redis_port,
        password=redis_password
)



app = Flask(__name__,
            static_url_path='/docs',
            static_folder='docs',
)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)


bootstrap = Bootstrap()

nav = Nav()
topbar = Navbar('',
    View('Home', 'index'),
    View('Profile', 'showprofile'),
)
nav.register_element('top', topbar)

@app.route('/')
def index():
   j = rdb.smembers("USERLIST")
   user_list = [x[1].decode('utf-8') for x in enumerate(j)]
   print(user_list)
   return render_template('index.html', userlist = user_list)

@app.route('/dologin', methods = ['POST'])
def dologin():
      form = request.form.to_dict()
      session['username'] = form['user']
      return redirect("/", code=302)

@app.route('/profile')
def showprofile():
   user=session.get('username')
   p = rdb.hgetall("user:{}".format(user))
   profile = {key.decode('utf-8'):int(value) for (key, value) in p.items()}

   return render_template(
         'userprofile.html',
         user=session.get('username'),
         profile=profile,
         )

if __name__ == '__main__':
   sess = Session(app)
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=8080, host="0.0.0.0")
