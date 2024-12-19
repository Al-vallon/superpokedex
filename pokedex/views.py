from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.


# def test_co(request):
#     return HttpResponse("Les connexions fonctionnent correctement.")

def getAllPokemon(request):
    url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(url, params={"limit": 151})
    if response.status_code == 200:
        data = response.json()
        pokemons = data.get("results", [])
        return render(request, "pokedex.html", {"pokemons": pokemons})
    else:
        return HttpResponse("Pokémons not found", status=404)

def getPokemonById(request, id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"data: {data}")
        return render(request, "pokemon.html", {"pokemon": data})
    else:
        return HttpResponse("Pokémon not found", status=404)
    
    
    

def custom_404(request, exception):
    return render(request, '404.html', status=404)