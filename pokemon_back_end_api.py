import requests

#
# The API should respond with the following information:
# - The Pokémon ID.
# - The silhouette image of the Pokémon.
# - A list of four Pokémon names (the correct name and three decoy names)
#

# https://pokeapi.co/

base_url = "https://pokeapi.co/api/v2"

def getPokemonInfo(name):
    url = "{}/pokemon/{}".format(base_url, name)
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        print("Success: data retrieved")
    else:
        print("Failed to get data, error code: {}".format(response.status_code))

    return response.json()

pokemonName = "pikachu"
pokemonInfo = getPokemonInfo(pokemonName)

if pokemonInfo:
    print(pokemonInfo["name"])
    print(pokemonInfo["id"])
    print(pokemonInfo["sprites"]["front_default"])