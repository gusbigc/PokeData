import requests
import json
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request
"""
Flask é a "classe"  que vai criar a aplicação
render_template é uma função que pega um arquivo .html de dentro da pasta
templates e devolve ele como resposta
request é um objeto que representa o pedido que chegou de algem que acessou
o site
"""
app = Flask(__name__)
"""
isso criao objeto principal que representa a aplicacao web, o app vai ser usado
pra marcar quais funções sao rotas do site
"""

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
        
        """showImage(dadosDICT)"""
    else:
        print("Pokémon não foi encontrado.")

    return dadosDICT
    """
    necessario adicionar esse return pq o flask nao trabalha com o terminal,
    ou seja, ele quer receber os dados de volta pra mandar pra pagina web mostrar

    """

def showImage(dataDICT):
    imageLink = dataDICT["sprites"]["other"]["official-artwork"]["front_default"]
    imageAnswer = requests.get(imageLink)

    image = Image.open(BytesIO(imageAnswer.content))
    image.show()

def encounters(dadosDICT):
    url_encounters = dadosDICT["location_area_encounters"]
    dataEncounters = searchData(url_encounters)
    return dataEncounters

"""
nome = nomePokemon()
buscaPokemon(nome)
"""
@app.route("/")
def home():
    return render_template("site.html", pokemon=None, buscou=False)

@app.route("/buscar")
def buscar():
    nome = request.args.get("pokemon")
    dadosDICT = buscaPokemon(nome)
    return render_template("site.html", pokemon=dadosDICT, buscou=True)

if __name__ == "__main__":
    app.run(debug=True)
'''
@app.route("/") -> isso é um decorator(a etiqueta com @). ele diz que quando
alguem acessar a pagina raiz do site(/, ou seja, o endereço principal), exe-
cuta a funcao logo abaixo

return render_templates("site.html") -> pega o arquivo site.html e devolve
como resposta para o navegador

-//-

return render_template.... -> agora ele recebe um segundo argumento, pokemon=
dadosDICT, isso significa que esta mandando uma variavel pokemon pro html
,e o valor dela é o dadosDICT que a função buscaPokemon retornou. eh assim que
o html vai conseguir enxergar os dados do python, atraves do nome pokemon que es
ta sendo definido
'''