from django.urls import path
from . import views

urlpatterns = [
    # path('', views.test_co, name='test_co'), 
    path('pokemons', views.getAllPokemon, name='getAllPokemon'), 
    path('pokemons/<int:id>', views.getPokemonById, name='getPokemonById'),
]