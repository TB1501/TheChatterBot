from flask import render_template, redirect, url_for, flash, session

#Handling the registration
def handle_register(request, users):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists. Please log in.", "error")
            return redirect(url_for('login'))
        users[username] = password
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

#Handling the login
def handle_login(request, users):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('chat'))
        else:
            flash("Invalid credentials or unregistered user.", "error")
    return render_template('login.html')