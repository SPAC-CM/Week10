from flask import Flask,jsonify,request, make_response
from SQL_Manager import *
import os

#The api is based on python flask
app = Flask(__name__)
manager = SQL_Manager()
factory = Factory()

#To correclty handle requests from different domains, we need to set CORS allowence in our response
#Therefore all requests are sent with the OPTIONS method first to see if it is allowed to proceed

#For the options preflight we need to set allowence for origin, headers and methods
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

#For the actual response we need to set allowence for origin only
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def _return_error(error : str):
    response = make_response()
    response.status = 500
    response.response=str(error)
    return _corsify_actual_response(response)


#API call to add an element to the database
@app.route("/add",methods=["POST","OPTIONS"])
def add():

    #This check appers in all calls so I will explain it here and never again
    #A domain always sends an options preflight call just to check for CORS allowence. Thus we tell it that it is indeed allowed to call the method
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:

        #Gets the request body from the request
        data = request.get_json()

        #Tries to add elements to the database
        try:
            #Calls the factory class to create an element based on the request data
            element = factory.create_element(data)

            #Adds it to the database
            manager.add_item(element)

            #Creates a response
            response = make_response()
            response.status = 200

            #Returns the response allong with a CORS allowence
            return _corsify_actual_response(response)

        #If above failed we return an error
        except Exception as e:
            return _return_error(str(e))

#API call to login to get an autherization token
@app.route("/login",methods=["POST","OPTIONS"])
def login():
    
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    else:
        #Gets the request body
        data = request.get_json()
        try:

            #Checks credentials to the hardcoded SQL database credentials. Aka if the user could login to the database manualy they have autherization to do it on the frontend aswell
            if data["user"] != "root" and data["password"] != "SPAC-SQLBOI2024":
                raise Exception("Not autherized")

            #Creates the response
            response = make_response()

            #The token is just a random string 15 char long. I only encoded it in base64 because I find it funny that a hacker would decode it just to see that it is random garbage anyways
            response.response = str(os.urandom(15).hex())
            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            return _return_error(str(e))

#API call to get a specific table from the database
@app.route('/table', methods=['POST', 'OPTIONS'])
def get_table():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            #Gets response body
            content = request.get_json()

            #Gets the name of the table
            table_name = content["table_name"]

            #Gets the sql_alchemy representation of the table
            table = manager.get_table(table_name)

            #Payload is the response body essentailly.
            #We set the first index to be the keys of the table
            #Also for some reason (I have 0 clue as to why) but sql_alchemy returns strings with ', which is fine if it werent for the fact that react typescripts json parser can't decode it
            #Whic is actually even wierder since react can create strings based on ' but for some reason in the parser they did not add that symbol for string interpolation
            #Therefore I remove them
            payload = [str(manager.get_keys(table_name)).replace("'","").replace('"','')]
            for row in table:
                #Adds the rows of the table into the payload
                payload.append(str(row).replace('(',"[").replace(')',"]").replace("'",""))
            
            #creates the response
            response = make_response()
            response.status = 201

            #char(34) = " so if there where any evil ' left it will now be converted to a value the react json parser can eat
            response.response = str(payload).replace("'",chr(34))
            return _corsify_actual_response(response)
        except Exception as e:
            return _return_error(str(e))

#API call to upload an image to a specific demon
@app.route('/image', methods=['POST', 'OPTIONS'])
def uploade_image():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:

            #Gets the request body
            content = request.get_json()
            
            #The image is a base64 encoded string with a bunch of extra stuff we do not need
            base64 = content["data"].split(",")[1]
            response = make_response()

            #Updates the specific demon to now have that image
            manager.update_item("demon", "id", content["id"], "image", base64)

            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            return _return_error(str(e))

#API call to get an image of a specific demon
@app.route('/demon-pic', methods=['POST','OPTIONS'])
def get_image():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            #Gets request body
            content = request.get_json()
            response = make_response()

            #Gets the image from the manager
            payload = manager.get_chonked_image(content["id"])
            response.response = str(payload)
            response.status = 200
            return _corsify_actual_response(response)
        except Exception as e:
            return _return_error(str(e))

#Starts the API on local host with on the port 8080
if __name__=="__main__":
    app.run(host="127.0.0.1",port=8080)
