import requests
from flask import Flask, jsonify, send_from_directory, request
import random

app = Flask(__name__)

MAX_POKEMON = 50
NUM_DECOYS = 3
BASE_URL = "https://pokeapi.co/api/v2/"
SUCCESS = 200
INTERNAL_SERVER_ERROR = 500

def getPokemonInfo(pokemonId):
    response = requests.get("{}/pokemon/{}".format(BASE_URL, pokemonId))
    if response.status_code == SUCCESS:
        return response.json()
    else:
        return None

def getTrueName(pokemonId):
    pokemonInfo = getPokemonInfo(pokemonId)
    if pokemonInfo:
        return pokemonInfo["name"]
    else:
        return None

def getRandomPokemonId():
    return random.randint(1, MAX_POKEMON)

def getSilhouetteImage(pokemonInfo):
    return pokemonInfo["sprites"]["front_default"]

def getDecoyNames(correctName):
    decoyNames = set()
    while len(decoyNames) < NUM_DECOYS:
        pokemonId = getRandomPokemonId()
        name = getTrueName(pokemonId)
        if name and name != correctName:
            decoyNames.add(name)
    return list(decoyNames)

@app.route('/pokemon', methods=['GET'])
def getRandomPokemon():
    pokemonId = getRandomPokemonId()
    pokemonInfo = getPokemonInfo(pokemonId)

    if not pokemonInfo:
        return jsonify({"error": "Could not retrieve Pokémon info from pokeapi"}), INTERNAL_SERVER_ERROR
    
    silhouetteImage = getSilhouetteImage(pokemonInfo)
    trueName = getTrueName(pokemonId)
    decoyNames = getDecoyNames(trueName)
    
    pokemonNamesList = [trueName] + decoyNames
    random.shuffle(pokemonNamesList)

    return jsonify({
        "pokemonID": pokemonId,
        "silhouetteImage": silhouetteImage,
        "pokemonNamesList": pokemonNamesList
    })

@app.route('/verify', methods=['POST'])
def verifyGuess():
    data = request.get_json()
    pokemonId = data.get('pokemonID')
    guessedName = data.get('guessedName')

    trueName = getTrueName(pokemonId)
    pokemonInfo = getPokemonInfo(pokemonId)
    
    if pokemonInfo:
        fullImage = pokemonInfo["sprites"]["front_default"]
    else:
        fullImage = None
    
    isCorrect = (trueName == guessedName)

    return jsonify({
        "trueName": trueName,
        "fullImage": fullImage,
        "isCorrect": isCorrect
    })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=False)
