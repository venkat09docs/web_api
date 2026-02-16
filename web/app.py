from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.anewDB
UserNum = db["UserNum"]

UserNum.insert_one({ 'num_of_users' :0 })

class Visits(Resource):
    def get(self):
        prev_count = UserNum.find()[0]['num_of_users']
        new_count = prev_count + 1
        UserNum.update_one({}, {"$set":{"num_of_users":new_count}})
        return f"Number of visits" + f"{new_count}"


def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "a" not in postedData or "b" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "a" not in postedData or "b" not in postedData:
            return 301
        elif int(postedData["b"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        # Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")

        if (status_code!=200):
            retJson = {
                "Result": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        # If i am here, then status_code == 200
        a = int(postedData["a"])
        b = int(postedData["b"])

        ret = a + b

        retDict = {
            'Result': ret,
            'Status Code': 200
        }
        return jsonify(retDict)

class Sub(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        # Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")

        if (status_code!=200):
            retJson = {
                "Result": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        # If i am here, then status_code == 200
        a = int(postedData["a"])
        b = int(postedData["b"])

        ret = a - b

        retDict = {
            'Result': ret,
            'Status Code': 200
        }
        return jsonify(retDict)

class Multiply(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        # Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")

        if (status_code!=200):
            retJson = {
                "Result": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        # If i am here, then status_code == 200
        a = int(postedData["a"])
        b = int(postedData["b"])

        ret = a * b

        retDict = {
            'Result': ret,
            'Status Code': 200
        }
        return jsonify(retDict)

class Division(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        # Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")

        if (status_code!=200):
            retJson = {
                "Result": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        # If i am here, then status_code == 200
        a = int(postedData["a"])
        b = int(postedData["b"])

        ret = a / b

        retDict = {
            'Result': ret,
            'Status Code': 200
        }
        return jsonify(retDict)


api.add_resource(Add, "/api/v0/add")
api.add_resource(Sub, "/api/v0/sub")
api.add_resource(Multiply, "/api/v0/multiply")
api.add_resource(Division, "/api/v0/division")
api.add_resource(Visits, "/hello")

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)