import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv('/home/boudors6/Desktop/Cytailorv1.0/Cytailorv1.0/pyvenv.cfg')
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Love You Katkout <3 </h1>"


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    print(os.environ.get('test'))
