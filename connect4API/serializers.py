from rest_framework import serializers
from .models import Player, PlayerTurn

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'

class PlayerTurnSerializer(serializers.ModelSerializer):
	playerturn = serializers.StringRelatedField(many=True)
	class Meta:
		model = Player
		fields = ['player', 'playerturn']
