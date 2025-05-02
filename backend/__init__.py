from flask import Flask
from flask_migrate import Migrate
from .models import db
from .config import Config
from flask import session
from backend.models import User
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='../frontend',
        static_folder='../frontend',
    )

    app.config.from_object(Config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    # ✅ Auto-create DB if it doesn't exist
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                print("🆕 Creating new database:", db_path)
                db.create_all()
            else:
                print("✅ Database already exists:", db_path)

    # 📌 Inject `user` into all templates
    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if not user.avatar_path:
                user.avatar_path = 'asset/avatar.png'
        return dict(user=user)

    from .routes import register_routes
    register_routes(app)

    return app
