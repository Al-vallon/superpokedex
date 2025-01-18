from django.db import models

from pokedex.models.pokemon import Pokemon


class Teams(models.Model):
    name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon)
    
    def __str__(self):
        return self.name