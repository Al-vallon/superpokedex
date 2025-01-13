from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import requests

API_URL = "https://pokeapi.co/api/v2/pokemon/"

def getAllPokemon(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)
    
    try:
        response = requests.get(f"{API_URL}?offset={offset}&limit={limit}")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return HttpResponse("Pokémons not found", status=404)
    
    pokemons = data.get("results", [])
    next_offset = data.get("next", "").split("offset=")[-1].split("&")[0] if data.get("next") else None
    previous_offset = data.get("previous", "").split("offset=")[-1].split("&")[0] if data.get("previous") else None

    all_pokemons = []
    for pokemon in pokemons:
        pokemon_url = pokemon['url']
        try:
            response_pokemon = requests.get(pokemon_url)
            response_pokemon.raise_for_status()
            data_pokemon = response_pokemon.json()
            name = data_pokemon['name']
            image_url = data_pokemon['sprites']['front_default']
            all_pokemons.append({
                'name': name,
                'image_url': image_url,
            })
        except requests.exceptions.RequestException:
            continue  # Skip this Pokémon if there's an error

    return render(request, "pokedex.html", {
        'all_pokemons': all_pokemons,
        "next_offset": next_offset,
        "previous_offset": previous_offset,
        "current_offset": offset,
    })

def getPokemonById(request, id):
    url = f"{API_URL}{id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"data: {data}")
        return render(request, "pokemon.html", {"pokemon": data})
    else:
        return HttpResponse("Pokémon not found", status=404)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def searchPokemon(request):
    pokemon_name = request.GET.get("pokemon-name", "").strip()
    url = f"{API_URL}{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"data: {data}")
        return render(request, "pokemon.html", {"pokemon": data})
    else:
        return HttpResponse("Pokémon not found", status=404)
