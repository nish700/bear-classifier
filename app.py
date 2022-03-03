import flask
from flask import Flask , request , render_template, flash, redirect, url_for #jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
import pandas
import pickle
import shutil


app = Flask(__name__)
model = pickle.load(open('rf_model', 'rb'))

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output_pred = ""
    output = prediction[0]
    

    if int(output) == 1:
    	output_pred= "YES"
    else:
    	output_pred = "NO"

    return render_template('main.html', prediction_text=f'Will the Insurer claim the Insurance: {output_pred}')


if __name__ == "__main__":
    app.run(debug=True)