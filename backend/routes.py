from .functions import *

# This file contains the routes for the Flask application.
def register_routes(app):
    # The home route renders the index.html template.
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return handle_login()

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return handle_register()
