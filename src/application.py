from flask import Flask
from src.endpoints import api_blueprint
from src.infoapi import version
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="/api" + version)
app.config['JWT_SECRET_KEY'] = 'JWTKEY2019*@#$PriceBUDDYLMTSCorp198519891998'

jwt = JWTManager(app)

@app.route("/")
def index():
    return "Home"

@app.route("/teste")
def teste():
    return "Teste"

if __name__ == '__main__':
    app.run(debug=True)