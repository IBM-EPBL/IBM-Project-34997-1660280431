import numpy as np
from flask import Flask, render_template, request
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "P-v0uUtXoamzjb6MZFyGXQnh9ql2xObgQaTMWSjkbXJg"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
model = pickle.load(open('wqi.pkl','rb'))
@app.route('/')
def home():
    return render_template("index.html",)
@app.route('/login' ,methods = ['POST'])
def login():
    year = request.form["year"]
    do = request.form["do"]
    ph = request.form["ph"]
    co = request.form["co"]
    bod = request.form["bod"]
    na = request.form["na"]
    tc = request.form["tc"]
    total = [[float (do), float (ph), float (co), float (bod), float (na), float(tc), int(year)]]
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [float (do), float (ph), float (co), float (bod), float (na), float(tc), int(year)], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/823bcd15-d246-4027-ae6d-a984d3e1b053/predictions?version=2022-11-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    predict = int(predictions['predictions'][0]['values'][0][0])
    #print("Final prediction :",predict)

    if(predict >= 95 and predict<= 100) :
        return render_template("index.html", showcase = 'Excellent, The predicted value is '+str(predict))
    elif(predict >= 89 and predict <= 94) :
        return render_template("index.html", showcase = 'Very good, The predicted value is '+str(predict))
    elif(predict >= 88 and predict <= 88) :
        return render_template("index.html", showcase = 'Good, The predicted value is '+str(predict))
    elif(predict >= 65 and predict <= 79) :
        return render_template("index.html", showcase = 'Fair, The predicted value is '+str(predict))
    elif(predict >= 45 and predict <= 64) :
        return render_template("index.html", showcase = 'Marginal, The predicted value is '+str(predict))
    else :
        return render_template("index.html", showcase = 'Poor, The predicted value is '+str(predict))
if __name__=='__main__' :
    app.run(debug = True,port=500)