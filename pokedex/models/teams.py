from django.db import models
from django.core.exceptions import ValidationError

from pokedex.models.pokemon import Pokemon


class Teams(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon)
    
    #check if 6 poke in team
    # def checkNbPokemons(self):
    #     if self.pokemons.count() > 6:
    #         return ValidationError('You must have 6 pokemons in your team')
    
    # def save(self, *args, **kwargs):
    #     self.checkNbPokemons()
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return (self.id, 'Team: ' + self.name) 