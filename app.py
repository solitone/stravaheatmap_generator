# You need to create a stravalogin.py file in the app root directory
# defining the following variables:
#
# STRAVA_USR = "<YOUR_STRAVA_USERNAME>"
# STRAVA_PWD = "<YOUR_STRAVA_PASSWORD>"
#
import stravalogin 
import json
import secrets
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from urllib.parse import quote, unquote
from flask_babel import Babel, gettext  # for translations
from urllib.parse import urlparse, urljoin
from stravaheatmap.cartograph.onlinemap import OnlineMap

app = Flask(__name__)
# generate a random secret key of 32 characters (32 hexadecimal digits
app.config['SECRET_KEY'] = secrets.token_hex(16)  
babel = Babel(app)
babel = Babel(app)

def get_locale():
    if 'lang' in session:
        return session['lang']    
    return request.accept_languages.best_match(['it', 'en']) # returns best language for user

babel.init_app(app, locale_selector=get_locale)

@app.route('/lang/<lang>')
def set_lang(lang=None):
    session['lang'] = lang
    referrer = request.referrer
    if referrer is not None and is_safe_url(referrer):
        return redirect(referrer)
    else:
        return redirect(url_for('home'))

def is_safe_url(target):
    """
    Ensure the target url is safe and redirect there:
    check that the url the user is redirected to 
    does not come from an external site, thus avoiding 
    potential phishing attacks or other types. 
    If the url is not safe or does not exist, 
    the user is redirected to the homepage.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# To use a Python function in a Jinja2 template,
# we need to pass that function to the template's context.
# With the following snippet function get_locale will be available in all templates
@app.context_processor
def inject_functions():
    return dict(get_locale=get_locale)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
         json_string, error_string = get_json_string()
         if error_string == "":
            return render_template('index.html', page='home', json_string=json_string)
         else:
            return render_template('index.html', page='home', error_message=error_string) 
    
    return render_template('index.html', page='home')

@app.route('/howto', methods=['GET', 'POST'])
def howto():
    if request.method == 'POST':
         json_string, error_string = get_json_string()
         if error_string == "":
            return render_template('howto.html', page='howto', json_string=json_string)
         else:
            return render_template('howto.html', page='howto', error_message=error_string) 
    
    return render_template('howto.html', page='howto')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
         json_string, error_string = get_json_string()
         if error_string == "":
            return render_template('contacts.html', page='contacts', json_string=json_string)
         else:
            return render_template('contacts.html', page='contacts', error_message=error_string) 
    
    return render_template('contacts.html', page='contacts')

@app.route('/download', methods=['POST'])
def download():
    json_string = request.form.get('json_string')
    if json_string:
        # Decodifica la stringa JSON precedentemente codificata
        decoded_json_string = unquote(json_string)
        
        # Restituzione del file JSON come risposta
        response = make_response(decoded_json_string)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename=carto_strava.onlinemap'

        return response

    return gettext("Errore nel download del file.")

def get_json_string():
        color = request.form.get('color')
        if color in ['hot', 'blue', 'purple', 'gray', 'red']:
            # Creazione della heatmap e generazione del file JSON
            definition = OnlineMap.getDefinition(color, stravalogin.STRAVA_USR, stravalogin.STRAVA_PWD)
            # Conversione dell'oggetto definition in una stringa JSON
            json_string = json.dumps(definition)
            
            # Codifica la stringa JSON per evitare troncamenti
            encoded_json_string = quote(json_string)

            return encoded_json_string, ""
        
        else:
            # Creazione del messaggio di errore JSON
            error_message = {'error': 'Colore non valido'}
            error_json_string = json.dumps(error_message)

            return "", error_json_string

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5555)
