# You need to create a stravalogin.py file in the app root directory
# defining the following variables:
#
# STRAVA_USR = "<YOUR_STRAVA_USERNAME>"
# STRAVA_PWD = "<YOUR_STRAVA_PASSWORD>"
#
import stravalogin 
import json
from flask import Flask, render_template, request, make_response
from urllib.parse import quote, unquote

from stravaheatmap.cartograph.onlinemap import OnlineMap

app = Flask(__name__)

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

    return "Errore nel download del file."

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
    app.run(debug=True, port=5555)
