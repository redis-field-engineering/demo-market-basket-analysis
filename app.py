from flask import Flask, render_template, request, redirect, session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_session import Session

import redis
from os import environ
import redisai

from ai_setup import setup_ai

CATEGORIES = [
 "Apparel", "Automotive", "Baby", "Beauty", "Books", "Camera",
 "Digital_Ebook_Purchase", "Digital_Music_Purchase", "Digital_Software", "Digital_Video_Download", "Digital_Video_Games",
 "Electronics", "Furniture", "Gift_Card", "Grocery", "Health_Personal_Care", "Home_Entertainment",
 "Home_Improvement", "Home", "Jewelry", "Kitchen", "Lawn_and_Garden", "Luggage",
 "Major_Appliances", "Mobile_Apps", "Mobile_Electronics", "Musical_Instruments", "Music", "Office_Products",
 "Outdoors", "PC", "Personal_Care_Appliances", "Pet_Products", "Shoes", "Software", "Sports", "Tools", "Toys", "Video_DVD",
 "Video_Games", "Video", "Watches", "Wireless"
]


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

# Flush on startup
rdb.flushdb()

app = Flask(__name__,
            static_url_path='/docs',
            static_folder='docs',
)

SESSION_TYPE = 'redis'
SESSION_REDIS = rdb
app.config.from_object(__name__)


bootstrap = Bootstrap()

nav = Nav()
topbar = Navbar('',
    View('User', 'index'),
    View('Profile', 'showprofile'),
    View('Cart', 'showcart'),
)
nav.register_element('top', topbar)

def get_profile(user):
   p = rdb.hgetall("user:{}".format(user))
   profile = {key.decode('utf-8'):int(value) for (key, value) in p.items()}
   return(profile)

@app.route('/')
def index():
   if rdb.exists("USERLIST") < 1:
      setup_ai()
   j = rdb.smembers("USERLIST")
   user_list = [x[1].decode('utf-8') for x in enumerate(j)]
   return render_template('index.html', userlist = user_list)

@app.route('/dologin', methods = ['POST'])
def dologin():
      form = request.form.to_dict()
      session['username'] = form['user']
      return redirect("/profile", code=302)

@app.route('/profile')
def showprofile():
   user=session.get('username')
   profile = get_profile(user)

   if not user:
      return redirect("/", code=302)

   return render_template(
         'userprofile.html',
         user=session.get('username'),
         profile=profile,
         )

@app.route('/cart')
def showcart():
   user=session.get('username')

   if not user:
      return redirect("/", code=302)

   p = rdb.hgetall("user:{}".format(user))
   profile = {key.decode('utf-8'):int(value) for (key, value) in p.items()}

   return render_template(
         'usercart.html',
         user=session.get('username'),
         profile=profile,
         )

@app.route('/scorecart', methods = ['POST'])
def scorecart():
      form = request.form.to_dict()
      tnsr_name = "TENSOR:{}".format(session.sid)
      tnsr = []
      for c in CATEGORIES:
         if c in form:
            tnsr.append(float(form[c]))
         else:
            tnsr.append(float(0))

      conn.tensorset(tnsr_name, tnsr, shape=[1, 43],dtype='float')
      profile_results = conn.modelrun('profile_model', tnsr_name, "{}:results".format(tnsr_name))
      res = conn.tensorget("{}:results".format(tnsr_name))[0][0]

      #cleanup any tensors
      conn.delete(tnsr_name)
      conn.delete("{}:results".format(tnsr_name))

      profile=get_profile(session.get('username'))
      return render_template(
            'scoredcart.html',
            user=session.get('username'),
            cart=form,
            profile=profile,
            score=res
            )



if __name__ == '__main__':
   sess = Session(app)
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=8080, host="0.0.0.0")
