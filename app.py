from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/lougar")
def lougar():
    return render_template('lougar.html')

@app.route("/bodas")
def bodas():
    return render_template('gifts.html')

@app.route("/rsvp")
def rsvp():
    return render_template('rsvp.html')\

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        return render_template("thanks.html")


if __name__ == "__main__":
    app.run()
