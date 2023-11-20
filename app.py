from flask import Flask, render_template, request, jsonify, url_for
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# API information
API_URL = "https://api.petfinder.com/v2/animals"
TOKEN_EXPIRATION = 3600  # 1 hour

def refresh_api_key():
    print("-------------refresh_api_key----------")
    data = {
      'grant_type': 'client_credentials',
      'client_id': 'xsip0EE30bRUf4qpTyhk7rD4TaIOzX76KvTRTFMWLa2hb7E6uN',
      'client_secret': 'xvuoGGpxn73rrVTJd8OVezMGtrem7MwDwqRIsdpq'
    }
    response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
    response = response.json()
    access_token = response.get('access_token')
    app.api_key_refreshed_at = datetime.utcnow()
    app.api_key = access_token
    return access_token

app.api_key_refreshed_at = datetime.utcnow() - timedelta(hours=1, minutes=0)


@app.route('/')
def homepage():
    print("Homepage Visited")
    return render_template("index.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Extract form data
        pet_type = request.form.get('type')
        gender = request.form.get('gender')
        age = request.form.get('age')
        size = request.form.get('size')

        # Redirect to the /data route with search parameters
        return redirect(url_for('get_data', type=pet_type, gender=gender, age=age, size=size))
    else:
        return render_template("search.html")


@app.route("/shelters")
def shelter():
    print("Shelters Visited!")
    return render_template("shelters.html")

@app.route("/signup", methods=('GET', 'POST'))
def signup():
    print("Signup Visited!")
    return render_template("signup.html")

@app.route("/others")
def others():
    print("Others Visited!")
    return render_template("signup.html")

@app.route("/login")
def login():
    print("Login Visited!")
    return render_template("login.html")

@app.route("/donate")
def donate():
    print("Donate Visited!")
    return render_template("donate.html")

@app.route("/dogs")
def dogs():
    print("Dogs Visited!")
    return render_template("dogs.html")

@app.route("/cats")
def cats():
    print("Cats Visited!")
    return render_template("cats.html")

# Route for fetching data with filters

@app.route('/data', methods=['GET'])
def get_data():
    # Check if the third-party API key is still valid, refresh if necessary
    if (datetime.utcnow() - app.api_key_refreshed_at > timedelta(
                seconds=TOKEN_EXPIRATION)):
        app.api_key = refresh_api_key()
        app.api_key_refreshed_at = datetime.utcnow()

    params = []
    if request.args.get('type'):
        params.append(('type', request.args.get('type')))

    if request.args.get('gender'):
        params.append(('gender', request.args.get('gender')))

    if request.args.get('age'):
        params.append(('age', request.args.get('age')))

    if request.args.get('size'):
        params.append(('size', request.args.get('size')))

    headers = {'Authorization': f'Bearer {app.api_key}'}

    response = requests.get(API_URL, headers=headers, params=tuple(params))
    pets_data = response.json().get('animals', [])

    return render_template('results.html', pets_data=pets_data)


@app.route("/contact-us")
def contact_us():
    print("Contact-us Visited!")
    return render_template("contact-us.html")

@app.route("/others/birds")
def birds():
    print("Birds Visited!")
    return render_template("others/birds.html")

@app.route("/others/guinea-pig")
def guinea_pig():
    print("Guinea Pig Visited!")
    return render_template("others/guinea-pig.html")

@app.route("/others/rabbits")
def rabbits():
    print("Rabbits Visited!")
    return render_template("others/rabbits.html")

@app.route("/others/reptiles")
def reptiles():
    print("Reptiles Visited!")
    return render_template("others/reptiles.html")



if __name__ == "__main__":
    print("**App has started**")
    app.run(debug=True, use_reloader=True)