from flask import Flask, request, render_template, redirect, url_for, session
from logic.auth import handle_login,handle_register
from logic.pdf_handler import process_pdf
from logic.qa import answer_query



#Import the Flask web framework
app = Flask(__name__)
app.secret_key = 'test_secret_key'

#Simulated db for Users
users={}


#Route to home
@app.route('/')
def home():
    return render_template('home.html')

#Route to registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return handle_register(request, users)

#Route to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login(request, users)

#Handling the logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

#Route to main page
@app.route('/chat')
def chat():
    return render_template('chat.html')



@app.route("/ask", methods=["POST"])
def askPost():
        return answer_query(request)


@app.route("/pdf", methods=["POST"])
def pdfPost():
    return process_pdf(request)

def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()