from flask import Flask, render_template
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    sku = db.Column(db.String(15), unique=True)
    typeName = db.Column(db.String(30))

with app.app_context():
    db.create_all()


@app.route('/create_product/<productName>/<productSku>/<productTypeName>/', methods=['POST'])
@cross_origin()
def create_product(productName, productSku, productTypeName):
    try:
        credentials = {
            "Username": "logs@krameramerica.com",
            "Password": "KramerAmericaTest1",
            "Content-Type": "application/json"
        }

        auth_url = "https://smartline-trial.api.sellercloud.us/rest/api/token"
        products_url = "https://smartline-trial.api.sellercloud.us/rest/api/Products"
        payload = {
            "CompanyId": 163,
            "ProductName": productName,
            "ProductSKU": productSku,
            "ProductTypeName": productTypeName
            }

        response = requests.post(auth_url, credentials)

        if response.status_code == 200:

            response_json = response.json()
            token = response_json.get("access_token")

            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                 "Accept": "application/json"}
            

            # Uncomment this to test the database
            # ------------------------------------------------------------------------------

            # product = Product(name=productName, sku=productSku, typeName=productTypeName)
            # db.session.add(product)
            # db.session.commit()
            
        
            # This is where I got stock-------------------------------------------
            try:

                responseNext = requests.post(products_url, headers=headers, json=payload)

            except Exception as e:
                print(f"Error occurred when creating product: {e}")
        

            if responseNext.status_code == 200:
                print("Product created!!")

                print('Adding product to database')
                product = Product(name=productName, sku=productSku, typeName=productTypeName)
                db.session.add(product)
                db.session.commit()


                return "Product created!!"
            
                
            else:
                print("Product creation failed with status code:", response.status_code)
                return "Product creation failed"

        else:
            print("Authentication request failed with status code:", response.status_code)
            return "Authentication request failed"

        

    except Exception as e:
            print("Error:", str(e))
            return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(debug=True)