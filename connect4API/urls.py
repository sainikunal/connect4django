from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home_view),
    path('check_game_begin/', views.checkGameBegin),
    path('validate_move/', views.validateMove),
    path('check_game_won/', views.checkGameWon),

    path('api/', views.apiOverview, name="api-overview"),
    path('api/player-list/', views.playerList, name="player-list"),
    path('api/player/<int:playerId>/', views.playerView, name="player-view"),
]