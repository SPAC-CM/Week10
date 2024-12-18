from flask import Flask,jsonify,request, make_response
from SQL_Manager import *
import os

app = Flask(__name__)
manager = SQL_Manager()
factory = Factory()


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/add",methods=["POST","OPTIONS"])
def add():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        data = request.get_json()
        try:
            element = factory.create_element(data)
            manager.add_item(element)
            response = make_response()
            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            response = make_response()
            response.status = 500
            response.response=str(e)
            return _corsify_actual_response(response)

@app.route("/login",methods=["POST","OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        data = request.get_json()
        try:
            if data["user"] != "root" and data["password"] != "SPAC-SQLBOI2024":
                raise Exception("Not autherized")
            response = make_response()
            response.response = str(os.urandom(15).hex())
            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            response = make_response()
            response.status = 500
            response.response=str(e)
            return _corsify_actual_response(response)

@app.route('/table', methods=['POST', 'OPTIONS'])
def get_table():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            content = request.get_json()
            table_name = content["table_name"]
            table = manager.get_table(table_name)
            payload = [str(manager.get_keys(table_name)).replace("'","").replace('"','')]
            for row in table:
                payload.append(str(row).replace('(',"[").replace(')',"]").replace("'",""))
            response = make_response()
            if table_name.lower() == "demons" or table_name.lower() == "demon":
                response.headers.add("Image","Yepperoni")
            response.status = 201
            response.response = str(payload).replace("'",chr(34))
            return _corsify_actual_response(response)
        except Exception as e:
            response = make_response()
            response.status = 500
            response.response = str(e)
            return _corsify_actual_response(response)

@app.route('/image', methods=['POST', 'OPTIONS'])
def uploade_image():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            content = request.get_json()
            base64 = content["data"].split(",")[1]
            response = make_response()
            manager.update_item("demon", "id", content["id"], "image", base64)

            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            response = make_response()
            response.status = 500
            response.response = str(e)
            return _corsify_actual_response(response)

@app.route('/demon-pic', methods=['POST','OPTIONS'])
def get_image():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            content = request.get_json()
            response = make_response()
            payload = manager.get_chonked_image(content["id"])
            response.response = str(payload)
            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            response = make_response()
            response.status = 500
            response.response = str(e)
            return _corsify_actual_response(response)

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8080)
