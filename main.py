from flask import Flask
from routes.token import token_bp
from routes.discount import discount_bp
from routes.dao import dao_bp  # додаємо DAO

app = Flask(__name__)
app.register_blueprint(token_bp)
app.register_blueprint(discount_bp)
app.register_blueprint(dao_bp)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
