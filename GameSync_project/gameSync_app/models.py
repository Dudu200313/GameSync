from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    last_name = None
    first_name = None 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class game_cache(models.Model):
    game_name = models.TextField()
    game_platform = models.TextField()
    game_genre = models.TextField()

class Logview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_id = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    rating = models.FloatField(choices=[(x * 0.5, str(x * 0.5)) for x in range(1, 11)], blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_name = models.TextField()
    game_id = models.IntegerField()  # ID do jogo na API IGDB
    cover_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game_id')  # Evita duplicatas

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_name = models.TextField()
    game_id = models.IntegerField()  # ID do jogo na API IGDB
    cover_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game_id')  # Evita duplicatas

class Owned(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_name = models.TextField()
    game_id = models.IntegerField()  # ID do jogo na API IGDB
    cover_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game_id')  # Evita duplicatas