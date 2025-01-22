from django.db import models
from django.core.exceptions import ValidationError

class Teams(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    pokemon_1 =  models.CharField(null=True, blank=True, max_length=100)
    pokemon_2 =  models.CharField(null=True, blank=True, max_length=100)
    pokemon_3 =  models.CharField(null=True, blank=True, max_length=100)
    pokemon_4 =  models.CharField(null=True, blank=True, max_length=100)
    pokemon_5 =  models.CharField(null=True, blank=True, max_length=100)
    pokemon_6 =  models.CharField(null=True, blank=True, max_length=100)

    # pokemons = models.ManyToManyField(Pokemon)
    
    #check if 6 poke in team
    # def checkNbPokemons(self):
    #     if self.pokemons.count() > 6:
    #         return ValidationError('You must have 6 pokemons in your team')
    
    # def save(self, *args, **kwargs):
    #     self.checkNbPokemons()
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return (self.id, 'Team: ' + self.name) 