from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\self\backend\flask\PluralsightFlaskAPI\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False