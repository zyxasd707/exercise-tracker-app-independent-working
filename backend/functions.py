# This file contains the functions used in the backend of the application.

from flask import request, jsonify, render_template

def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = is_admin(username, password)
        return jsonify(success=admin, is_admin=admin)
    return render_template('login.html')

def handle_register():
    # TODO: Implement registration modal
    return render_template('register.html')

# This function checks if the user is an admin.
def is_admin(username, password):
    return username == "admin" and password == "admin"
