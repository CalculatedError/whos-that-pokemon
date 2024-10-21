import requests

#
# The API should respond with the following information:
# - The Pokémon ID.
# - The silhouette image of the Pokémon.
# - A list of four Pokémon names (the correct name and three decoy names)
#

def getRandomPokemon():
    pokemonID = getPokemonID()
    silhouetteImage = getSilhouetteImage()
    decoyNames = getDecoyNames()
    pokemonNamesList = trueName + decoyNames

    return jsonify({"pokemonID": pokemonID
                    "silhouetteImage": silhouetteImage
                    "decoyNames": decoyNames
                    "pokemonNamesList" = pokemonNamesList
                    })

