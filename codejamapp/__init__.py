from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path, 'codejam.sqlite'),
        SECRET_KEY="dev"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import database
    database.init_db()
    database.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')
    app.add_url_rule('/', 'index')

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/user')
    def user():
        return render_template('user.html')

    return app

# if __name__ == "__main__":
#     app.run("0.0.0.0", 5000, debug=True)