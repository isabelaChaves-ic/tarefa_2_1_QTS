from flask import Flask, render_template
from app.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_bp)

    @app.route("/status")
    def status():
        return {"status": "ok"}

    @app.route("/hello")
    def hello():
        return {"message": "Hello World"}

    @app.route("/")
    def index():
        return render_template("users.html")

    return app
