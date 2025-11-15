from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt
import string

#Creates a flask object and includes Bcrypt encryption on it
app = Flask(__name__)
bcrypt = Bcrypt(app)

#A link that routes the user to the login page
@app.route("/")
def home_page():
    return 'Welcome to the home page! Here is the link to the login page: <a href=\"/login\">Login</a>'

#Login page that takes in user input for a username and password
@app.route('/login', methods=["GET"])
def login_form():
    form_html = '''
    <form method="POST" action="/login">
        <h1>Login Form</h1>
        <h2>Enter username and password</h2>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Login</button>
    </form>
    '''
    return render_template_string(form_html)

#Dispalys the entered in username and hashed password; validates username and password
@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    #Checks that no special characters are in the username
    for i in username:
        if i not in string.ascii_letters and i not in string.digits:
            return 'Invalid Username. Cannot include special characters or spaces.'

    #Checks to see if the password is at least 8 characters
    if len(password) <= 7:
        return 'Invalid password. Must be at least 8 characters long. Link to return to login page: <a href=\"/login\">Login</a>'

    #Checks that the password only includes valid letters and numbers
    letters = False
    numbers = False
    for j in password:
        if j in string.ascii_letters:
            letters = True
        if j in string.digits:
            numbers = True

    #Checks if the password contains both letters and numbers; then displays what the user entered
    if letters and numbers:
        hashed_password = bcrypt.generate_password_hash(password.encode("utf8"))
        return render_template_string('''
        <h2>Login Credentials</h2>
        <p>Username: {{ u }}</p>
        <p>Password: {{ p }}</p>
        <p>Hashed password: {{ hp }}</p>
        <a href=\"/login\">Login Page</a>
        ''', u=username, p=password, hp=hashed_password)
    else:
        return 'Invalid Password. Must contain letters and numbers. Link to return to login page: <a href=\"/login\">Login</a>'

if __name__ == '__main__':
    app.run(debug=True)