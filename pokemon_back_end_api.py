import requests
import flask
from flask import jsonify

MAX_POKEMON = 50

#
# The API should respond with the following information:
# - The Pokémon ID.
# - The silhouette image of the Pokémon.
# - A list of four Pokémon names (the correct name and three decoy names)
#
def getTrueName(pokemonID):
    # TODO REPLACE WITH API CALL
    return "bulbosaur"

def getRandomPokemonID():
    return random.randint(0, MAX_POKEMON - 1) 

def getSilhouetteImage(pokemonID):
    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png"

def getDecoyNames():
    return ["pikachu", "crosshairs", "gregosaur"]

@app.route('/pokemon', methods=['GET'])
def getRandomPokemon():
    pokemonID = getRandomPokemonID()
    silhouetteImage = getSilhouetteImage(pokemonID)
    decoyNames = getDecoyNames()
    trueName = getTrueName(pokemonID)
    pokemonNamesList = [trueName] + decoyNames 

    return {"pokemonID": pokemonID,
            "silhouetteImage": silhouetteImage,
            "pokemonNamesList": pokemonNamesList
    }

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)