import requests
import flask
from flask import jsonify
from flask import Flask

from flask import Flask, jsonify, send_from_directory
import random

MAX_POKEMON = 50
baseUrl = "https://pokeapi.co/api/v2/"

app = Flask(__name__)

#
# The API should respond with the following information:
# - The Pokémon ID.
# - The silhouette image of the Pokémon.
# - A list of four Pokémon names (the correct name and three decoy names)
#

def getPokemonInfo(id):
    url = "{}/pokemon/{}".format(baseUrl, id)
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        print("Success: data retrieved")
    else:
        print("Failed to get data, error code: {}".format(response.status_code))

    return response.json()

def getTrueName(pokemonID):
    # TODO REPLACE WITH API CALL
    return "bulbosaur"

def getRandomPokemonID():
    return random.randint(1, MAX_POKEMON) 

def getSilhouetteImage(pokemonInfo, pokemonID):
    return pokemonInfo["sprites"]["front_default"]

def getDecoyNames():
    return ["pikachu", "crosshairs", "gregosaur"]

@app.route('/pokemon', methods=['GET'])
def getRandomPokemon():
    pokemonID = getRandomPokemonID()
    pokemonInfo = getPokemonInfo(pokemonID) 
    silhouetteImage = getSilhouetteImage(pokemonInfo, pokemonID)
    decoyNames = getDecoyNames()
    trueName = getTrueName(pokemonID)
    pokemonNamesList = [trueName] + decoyNames 

    return {"pokemonID": pokemonID,
            "silhouetteImage": silhouetteImage,
            "pokemonNamesList": pokemonNamesList
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)