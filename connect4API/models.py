from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=60)
    color = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.username

class PlayerTurn(models.Model):
	player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL, related_name='playerturn')
	moves = models.TextField(max_length=200)

