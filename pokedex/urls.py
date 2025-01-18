from django.urls import path

from . import views
from pokedex import teamsview

urlpatterns = [
    path('pokemons', views.getAllPokemon, name='getAllPokemon'), 
    path('pokemons/<int:id>', views.getPokemonById, name='getPokemonById'),
    path('search_pokemon/', views.searchPokemon, name='search_pokemon'),
    # path('teams', teamsview.manageTeam, name='manageTeam'),
]