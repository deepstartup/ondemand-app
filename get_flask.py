from flask import Flask
from flask import request
import json
from config import config
from postgre_conn_all import connect
import random, string
app = Flask(__name__)
######GetOps######