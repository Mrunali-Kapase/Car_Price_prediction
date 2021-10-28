import flask
from flask import Flask, render_template, request
import joblib

model = joblib.load('car_pred.pkl')

#initializing the flask
app = Flask(__name__)

@app.route('/')
def car_pred():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    Present_Price = request.form.get('Present_Price')
    Kms_Driven = request.form.get('Kms_Driven')
    Owner = request.form.get('Owner')
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')
    Seller_Type = request.form.get('Seller_Type')
    Transmission = request.form.get('Transmission')
    if(fuel_type=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(fuel_type=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
    if(Seller_Type=='Individual'):
        Seller_Type_Individual= 1
    else:
        Seller_Type_Individual= 0
    if(Transmission=='Manual'):
        Transmission_Manual =1
    else:
        Transmission_Manual =0
    current_year = 2021
    year = current_year-year

    prediction=model.predict([[Present_Price,Kms_Driven,Owner,year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
    output=round(prediction[0],2)
    if output<0:
        return render_template('home.html',prediction_text="Sorry you cannot sell this car")
    else:
        return render_template('home.html',prediction_text="You Can Sell The Car at {}".format(output), scroll="something") 

   
if __name__ == '__main__':
    app.run(debug=True)
