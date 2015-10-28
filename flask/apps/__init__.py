from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from app import e9
from app import viewtables
from app import edittables
