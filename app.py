# -*- coding: utf-8 -*-
"""RegexTask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VgWu9kLU36iJ5Q-z7kzHLK-u9CdTVrmM
"""
from flask import Flask, request, render_template,jsonify,send_file,redirect,session
import re
import json
from werkzeug.utils import secure_filename
from external_functions import probe_model_5l_profit


app = Flask(__name__)
app.secret_key = '123'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST','GET'])  
def success():  
    if request.method == 'POST':  
        file = request.files['file']
        json_input = file.read().decode('utf-8')
        data = json.loads(json_input)  # Parse the JSON input
        #print(data)
        # #id_list = [item['id'] for item in data] 
        # with open("data.json", "r") as file:
        #     content = file.read()
        #     # convert to json
        #     data = json.loads(content)
        result = probe_model_5l_profit(data["data"])
        print(result)
        session['result'] = result
        return redirect('/result')

        # file_path = './' + filename
        # with open(file_path, 'r') as file:
        #     json_str = file.read()
        # Create a response with appropriate headers to download the generated json file
        # response = app.response_class(
        #     response=result,
        #     status=200,
        #     mimetype='application/json',
        #     headers={'Content-Disposition': 'attachment;filename=finder.json'}
        # )

@app.route("/result")
def display():
    ds = session.get('result')
    return render_template('result.html',ds=ds)
if __name__ == "__main__":
    app.run()