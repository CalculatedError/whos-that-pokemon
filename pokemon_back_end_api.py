import requests
from flask import Flask, jsonify, send_from_directory, request
import random

app = Flask(__name__)

# Constants
maxPokemon = 50
numDecoys = 3
baseUrl = "https://pokeapi.co/api/v2/"

def getPokemonInfo(pokemonId):
    response = requests.get(f"{baseUrl}pokemon/{pokemonId}")
    return response.json() if response.status_code == 200 else None

def getTrueName(pokemonId):
    pokemonInfo = getPokemonInfo(pokemonId)
    return pokemonInfo["name"] if pokemonInfo else None

def getRandomPokemonId():
    return random.randint(1, maxPokemon)

def getSilhouetteImage(pokemonInfo):
    return pokemonInfo["sprites"]["front_default"]

def getDecoyNames(correctName):
    decoyNames = set()
    while len(decoyNames) < numDecoys:
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
        return jsonify({"error": "Could not retrieve Pokémon info"}), 500
    
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
    fullImage = pokemonInfo["sprites"]["front_default"] if pokemonInfo else None
    isCorrect = trueName == guessedName

    return jsonify({
        "trueName": trueName,
        "fullImage": fullImage,
        "isCorrect": isCorrect
    })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
