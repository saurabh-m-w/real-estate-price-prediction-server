from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
import imp

app = Flask(__name__)


__data_columns = json.load(open("columns.json", "r"))['data_columns']
__locations = __data_columns[3:]
__model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))

_data_columns2 = json.load(open("columns_pune.json", "r"))['data_columns']
__locations_pune = _data_columns2[3:]
__model_pune = pickle.load(open('pune_home_prices_model.pickle', 'rb'))



def get_estimated_price(model,data_columns,location,sqft,bhk,bath):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(model.predict([x])[0],2)
	




@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(__model,__data_columns,location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
	
@app.route('/predict_pune_home_price', methods=['GET', 'POST'])
def predict_pune_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(__model_pune,_data_columns2,location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

	


if __name__ == "__main__":
    app.run()