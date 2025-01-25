from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    last_name = None
    first_name = None 

# Depois organiza esse aqui, isso aqui é história kkkk...
class game_cache(models.Model):
    game_name = models.TextField()
    game_platform = models.TextField()
    game_genre = models.TextField()

class log(models.Model):  # Precisa estar definido antes de usar como FK
    date = models.DateTimeField(auto_now_add=True)

class analise(models.Model):
    log_fk = models.ForeignKey('log', on_delete=models.PROTECT)  # Usando string para referência
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

