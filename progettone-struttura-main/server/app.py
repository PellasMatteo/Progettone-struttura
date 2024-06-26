from flask import Flask, jsonify, request, json
from flask_cors import CORS
from pymongo import MongoClient
import os 
import redis




app = Flask(__name__)
CORS(app)

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/simple_json')
def simplejson():
    return jsonify({"valore" : "valore"})

#Creo una funzione che posso riciclare ogni volta che devo accedere al DB
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username= os.environ["MONGO_INITDB_ROOT_USERNAME"], 
                         password=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
                        authSource="admin")
    db = client[os.environ["MONGO_INITDB_DATABASE"]]
    return db

#Creo una route per ottenere tutti gli animali
@app.route('/animals')
def get_stored_animals():
    db=""
    #try:
    db = get_db()
    _animals = db.animal_tb.find()
    animals = [{"id": animal["id"], "name": animal["name"], "type": animal["type"]} for animal in _animals]
    return jsonify({"animals": animals})
    #except:
    #   pass
    #finally:
    #    if type(db)==MongoClient:
    #        db.close()



#Verifico di poter leggere le variabili d'ambiente impostate nel file docker-compose.yml
@app.route('/environment')
def env():
    return jsonify(
            {"env":[
                {"MONGO_INITDB_DATABASE": os.environ["MONGO_INITDB_DATABASE"]},
                {"MONGO_INITDB_ROOT_USERNAME": os.environ["MONGO_INITDB_ROOT_USERNAME"]},
                {"MONGO_INITDB_ROOT_PASSWORD": os.environ["MONGO_INITDB_ROOT_PASSWORD"]}
            ]})


    
@app.route('/newAnimal', methods = ['POST'])
def newAnimal():
    db=""
    db = get_db() #Ottengo l'istanza del DB
    #Cerco l'id maggiore 
    last_animal = db.animal_tb.find_one(sort=[("id", -1)])
    #print(last_animal, flush=True) # In caso di test aggiungere Flush
    #aggiorno l'id
    request.json['id'] = int(last_animal['id']) + 1 
    #inserisco la richiesta
    x = db.animal_tb.insert_one(request.json)
    #creo la risposta per il client
    resp = app.response_class(
        response= json.dumps({"id":request.json['id'], "name":request.json['id'], "type":request.json['type']}),
        status=200,
        mimetype='application/json'
    )
    return resp

def get_redis(): #Ottengo un'stanza della libreria redis
    return redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], db=0)

@app.route('/feedAnimal', methods = ['POST'])
def feedAnimal():
    r = get_redis()
    food_qty = r.incr(request.json['id'], 1)   #Incremeta la quantità di cibo fornita a un animale di una unità
    #print(food_qty, flush=True) # In caso di test aggiungere Flush
    resp = app.response_class(  #Creo una risposta da inviare al client come conferma
        response= json.dumps({"id":request.json['id'], "food_qty":food_qty}),
        status=200,
        mimetype='application/json'
    )
    return resp

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)



