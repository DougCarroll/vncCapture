from flask import Flask
from flask import request
   
app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")