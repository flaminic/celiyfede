from flask import Flask, render_template, request, redirect, url_for, make_response
from database import Database
from flask_basicauth import BasicAuth
import StringIO
import csv
import os

app = Flask(__name__)
database = Database()

app.config['BASIC_AUTH_USERNAME'] = os.getenv("USERNAME") or "test"
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("PASSWORD") or "password"

basic_auth = BasicAuth(app)

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

@app.route("/rsvp/<person_id>")
def edit_rsvp(person_id):
    person_details_info = database.get_person_details(person_id)
    if person_details_info:
        return render_template('editRsvp.html', person_details_info=person_details_info)
    else:
        return redirect(url_for('home'))

@app.route("/thanks/<person_id>")
def thanks(person_id):
    return render_template('thanks.html', person_id=person_id)

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        howmany = request.form['people']
        message = request.form['message'] or ""
        person_id = database.insert_person(
            first_name=first_name,
            last_name=last_name,
            email = email,
            howmany = howmany,
            message = message,
        )
        return redirect(url_for('thanks', person_id=person_id))\

@app.route("/register/<person_id>", methods=['POST'])
def modify_person(person_id):
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        howmany = request.form['people']
        message = request.form['message'] or ""
        database.edit_person(
            person_id,
            first_name=first_name,
            last_name=last_name,
            email = email,
            howmany = howmany,
            message = message,
        )
    return redirect(url_for('thanks', person_id=person_id))\

@app.route("/all-rsvp")
@basic_auth.required
def get_all_rsvp():
    rows = database.get_all_people();
    return render_template("allRsvp.html", rows=rows)


@app.route('/download-rsvp')
@basic_auth.required
def download():
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'firstName', 'lastName', 'email', 'howmany', 'message',])

    rows = database.get_all_people();
    for row in rows:
        cw.writerow([row['id'], row['firstName'], row['lastName'], row['email'], row['howmany'], row['message'],])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=rsvp.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    app.run()
