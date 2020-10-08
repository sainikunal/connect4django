from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
from .models import Player, PlayerTurn
from .serializers import PlayerSerializer, PlayerTurnSerializer

def home_view(request):
	chars = [chr(i) for i in range(97, 97+26)]
	num = random.randint(0, 25)
	redPlayer = (chars[num] + str(num) + ''.join(random.sample(chars, 4)))
	yellowPlayer = (chars[num % 3] + str(num+1) + ''.join(random.sample(chars*2, 4)))
	allUsers = Player.objects.all()
	for user in allUsers:
		if redPlayer != user.username:
			redPlayer, created = Player.objects.get_or_create(username=redPlayer, color='Red')
		if yellowPlayer != user.username:
			yellowPlayer, created = Player.objects.get_or_create(username=yellowPlayer, color='Yellow')
	if allUsers.first() is None:
		redPlayer, created = Player.objects.get_or_create(username=redPlayer, color='Red')
		yellowPlayer, created = Player.objects.get_or_create(username=yellowPlayer, color='Yellow')
	context = {'redPlayer': redPlayer, 'yellowPlayer': yellowPlayer, 
	'redPlayerId': redPlayer.id, 'yellowPlayerId': yellowPlayer.id}
	return render(request, 'connect4API/index.html', context)

def checkGameBegin(request):
	data = json.loads(request.body)
	storeClickedSquare(data['id'], data['currTurn'])
	if data['beginId'] == 0 and data['gameActive'] == True and data['start'] == 'START':
		return JsonResponse('READY', safe=False)
	else:
		return JsonResponse('', safe=False)

def storeClickedSquare(sqId, currentPlayer):
	players = Player.objects.all().order_by('-id')[:2]
	yPlayer = Player.objects.get(id=players[0].id)
	rPlayer = Player.objects.get(id=players[1].id)
	p = PlayerTurn.objects.all()
	if currentPlayer == 'R':
		for i in p:
			if i.player_id == rPlayer.id:
				i.moves = i.moves + ',' + str(sqId)
				i.save()
				return 
		turn = PlayerTurn.objects.get_or_create(player=rPlayer, moves=sqId)
	if currentPlayer == 'Y':
		for i in p:
			if i.player_id == yPlayer.id:
				i.moves = i.moves + ',' + str(sqId)
				i.save()
				return 
		turn = PlayerTurn.objects.get_or_create(player=yPlayer, moves=sqId)


def validateMove(request):
	data = json.loads(request.body)
	if data['id'] in data['rSquares'] or data['id'] in data['ySquares']:
		return JsonResponse('InValid Move', safe=False)
	else:
		return JsonResponse('Valid Move', safe=False)

def checkGameWon(request):
	data = json.loads(request.body)
	rSquares = data['rSquares']
	ySquares = data['ySquares']
	player = 'Yellow' if data['currTurn'] == 'Y' else 'Red'
	possibleWinningSquareCombos = data['possibleWinningSquareCombos']
	if data['currTurn'] == 'Y':
		for i in range(len(possibleWinningSquareCombos)):
			counter = 0
			for j in range(len(possibleWinningSquareCombos[i])):
				if possibleWinningSquareCombos[i][j] in ySquares:
					counter += 1
					if counter == 4:
						return JsonResponse({'player': player + ' Wins', 'id': i})
	if data['currTurn'] == 'R':
		for i in range(len(possibleWinningSquareCombos)):
			counter = 0
			for j in range(len(possibleWinningSquareCombos[i])):
				if possibleWinningSquareCombos[i][j] in rSquares:
					counter += 1
					if counter == 4:
						return JsonResponse({'player': player + ' Wins', 'id': i})

	return JsonResponse({'player': None})



@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/player-list/',
		}

	return Response(api_urls)

@api_view(['GET'])
def playerList(request):
	players = Player.objects.all().order_by('-id')
	serializer = PlayerSerializer(players, many=True)
	return Response(serializer.data)

# @api_view(['GET'])
def playerView(request, playerId):
	p = PlayerTurn.objects.all()
	foundId = 0
	for i in p:
		if i.player_id == playerId:
			foundId = i.id
			break

	moves = PlayerTurn.objects.get(id=foundId)
	return JsonResponse({'username': moves.player.username, 'playerId': playerId, 'moves': moves.moves, })