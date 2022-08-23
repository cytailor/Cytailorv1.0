# This is a sample Python script.
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/riskbase"
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Vulnerability(db.Model):
    __tablename__ = 'vulnerability'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    Description = db.Column(db.String())


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
