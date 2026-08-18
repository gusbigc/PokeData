import requests
import json
from PIL import Image
from io import BytesIO

def nomePokemon():
    nome = input("Digite o nome do pokémon que você quer pesquisar: ")
    return nome
 
def searchData(url):
    answer = requests.get(url)
    if answer.status_code == 200:
        return answer.json()
    else:
        print(f"Error in searching data: {answer.status_code}")
        return None
    
def buscaPokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{str(nome).lower()}"
    dadosDICT = searchData(url)

    if dadosDICT is not None:
        print(f"Nome do pokémon: {dadosDICT["name"]}")
        for tipo in dadosDICT["types"]:
            print(f"Tipo {tipo["slot"]}: {tipo["type"]["name"]}")
        print(f"Peso: {dadosDICT["weight"] / 10} kg")
        print(f"Altura: {dadosDICT["height"] / 10} m")
        EncountersJSON = encounters(dadosDICT)
        print("Encounter Areas:")

        for indice, encounter in enumerate(EncountersJSON, start=1):
            print(f"Area {indice}: {encounter["location_area"]["name"]}")

        for indice1, ability in enumerate(dadosDICT["abilities"], start=1):
            print(f"Ability {indice1}: {ability["ability"]["name"]}")

        for stats in dadosDICT["stats"]:
            print(f"{stats["stat"]["name"]}: {stats["base_stat"]}")
        for tipo in dadosDICT["types"]:
            print(tipo.keys())
        """showImage(dadosDICT)"""
    else:
        print("Pokémon não foi encontrado.")

def showImage(dataDICT):
    imageLink = dataDICT["sprites"]["other"]["official-artwork"]["front_default"]
    imageAnswer = requests.get(imageLink)

    image = Image.open(BytesIO(imageAnswer.content))
    image.show()

def encounters(dadosDICT):
    url_encounters = dadosDICT["location_area_encounters"]
    dataEncounters = searchData(url_encounters)
    return dataEncounters


nome = nomePokemon()
buscaPokemon(nome)