from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt
import string

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route("/")
def home_page():
    return 'Welcome to the home page! Here is the link to the login page: <a href=\"/login\">Login</a>'

@app.route('/login', methods=["GET"])
def login_form():
    form_html = '''
    <form method="POST" action="/login">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Login</button>
    </form>
    '''
    return render_template_string(form_html)

@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    for i in username:
        if i not in string.ascii_letters and i not in string.digits:
            return 'Invalid Username. Cannot include special characters or spaces.'

    if len(password) <= 7:
        return 'Invalid password. Must be at least 8 characters long.'

    letters = False
    numbers = False
    for j in password:
        if j in string.ascii_letters:
            letters = True
        if j in string.digits:
            numbers = True

    if letters and numbers:
        hashed_password = bcrypt.generate_password_hash(password.encode("utf8"))
        return f'Username: {username}, Password: {hashed_password}'
    else:
        return 'Invalid Password. Must contain letters and numbers.'

if __name__ == '__main__':
    app.run(debug=True)