from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class Employees(Resource):
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

class Employees_Name(Resource):
    def get(self, employee_id):
        print('Employee id:' + employee_id)
        result = {'data': {'id':1, 'name':'Balram'}}
        return jsonify(result)

class Test(Resource):
  def get(self):
    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery("""
        prefix h: <http://www.webofdata.fr/vocabulary#>
        select * where {
          ?x a h:Homme
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

class getPatients(Resource):
    def get(self):
        sparql = SPARQLWrapper("http://localhost:8080/sparql")
        sparql.setQuery("""
            select * 
            where {?x ?p ?y}
            }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
        

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_2
api.add_resource(Test, '/Test') # route_3
api.add_resource(getPatients, '/patients') # route_4



if __name__ == '__main__':
     app.run(port=5002)
