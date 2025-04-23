from flask import request, render_template

def init_dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')
    return render_template('login.html')
