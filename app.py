from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return  render_template('index.html')

@app.route("/lougar")
def lougar():
    return 'Put something here'

@app.route("/bodas")
def bodas():
    return 'Put something here'

@app.route("/rsvp")
def rsvp():
    return 'Put something here'


if __name__ == "__main__":
    app.run()
