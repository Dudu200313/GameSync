from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    last_name = None
    first_name = None 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

# Depois organiza esse aqui, isso aqui é história kkkk...
class game_cache(models.Model):
    game_name = models.TextField()
    game_platform = models.TextField()
    game_genre = models.TextField()

class review(models.Model):
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

class log(models.Model):  # Precisa estar definido antes de usar como FK
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review_fk = models.ForeignKey(review, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_name = models.TextField()
    game_id = models.IntegerField()  # ID do jogo na API IGDB
    cover_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game_id')  # Evita duplicatas
