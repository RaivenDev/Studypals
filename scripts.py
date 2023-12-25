from datetime import datetime

from factory import db
from main import app
from models import User

with app.app_context():
    print('Aqui vinha o codigo')