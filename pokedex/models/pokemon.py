from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    sp_atk = models.IntegerField()
    sp_def = models.IntegerField()
    speed = models.IntegerField()
    
    def __str__(self):
        return self.name