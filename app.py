from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from routes.auth      import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.medicines import medicines_bp
    from routes.suppliers import suppliers_bp
    from routes.stock     import stock_bp
    from routes.sales     import sales_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicines_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(sales_bp)

    # Root redirect
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()   # creates tables if they don't exist
    app.run(debug=True)
