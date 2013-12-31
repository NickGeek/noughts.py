import socket
import sys
import random
import time

server = raw_input("\n\nServer to connect to: ")
channel = "#noughts.py"
botnick = "noughts"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))																												 #connects to the server
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Wanna play noughts and crosses?\n")
irc.send("NICK "+ botnick +"\n")
irc.send("JOIN "+ channel +"\n")

gameStats = {}
noughts = []
crosses = []

#Functions
def startGame():
	start = random.randrange(2)
	table = {"1":"/","2":"/","3":"/","4":"/","5":"/","6":"/","7":"/","8":"/","9":"/"}

	if start == 0:
		#Noughts start
		startingTeam = "noughts"
	else:
		startingTeam = "crosses"

	global gameStats
	gameStats = {"starting":startingTeam, "table":table, "currentMove":startingTeam}

	#Announce the new game
	send("A new game has started. "+startingTeam+" starts.")
	send("Table:")
	send("+-----------+")
	send("| "+gameStats["table"]["1"]+" | "+gameStats["table"]["2"]+" | "+gameStats["table"]["3"]+" |")
	send("| "+gameStats["table"]["4"]+" | "+gameStats["table"]["5"]+" | "+gameStats["table"]["6"]+" |")
	send("| "+gameStats["table"]["7"]+" | "+gameStats["table"]["8"]+" | "+gameStats["table"]["9"]+" |")
	send("+-----------+")
	send("Key: o = nought, x = cross and / = neutral")
	send("Each item on the grid is numbered from left to right starting at 1")

	global noughts
	global crosses
	noughts = []
	crosses = []

def game(username):
	sendPrivateMessage(username, "Table:")
	sendPrivateMessage(username, "+-----------+")
	sendPrivateMessage(username, "| "+gameStats["table"]["1"]+" | "+gameStats["table"]["2"]+" | "+gameStats["table"]["3"]+" |")
	sendPrivateMessage(username, "| "+gameStats["table"]["4"]+" | "+gameStats["table"]["5"]+" | "+gameStats["table"]["6"]+" |")
	sendPrivateMessage(username, "| "+gameStats["table"]["7"]+" | "+gameStats["table"]["8"]+" | "+gameStats["table"]["9"]+" |")
	sendPrivateMessage(username, "+-----------+")
	sendPrivateMessage(username, "Key: o = nought, x = cross and / = neutral")
	sendPrivateMessage(username, "Current move: "+gameStats["currentMove"])

def announceGame():
	send("Table:")
	send("+-----------+")
	send("| "+gameStats["table"]["1"]+" | "+gameStats["table"]["2"]+" | "+gameStats["table"]["3"]+" |")
	send("| "+gameStats["table"]["4"]+" | "+gameStats["table"]["5"]+" | "+gameStats["table"]["6"]+" |")
	send("| "+gameStats["table"]["7"]+" | "+gameStats["table"]["8"]+" | "+gameStats["table"]["9"]+" |")
	send("+-----------+")
	send("Key: o = nought, x = cross and / = neutral")
	send("Current move: "+gameStats["currentMove"])

def sendPrivateMessage(username, message):
	irc.send('PRIVMSG '+sender+' :'+message+'\n')
def send(message):
	irc.send('PRIVMSG '+channel+' :'+message+'\n')

def gameover():
	if gameStats["table"]["1"] == gameStats["table"]["2"] and gameStats["table"]["2"] == gameStats["table"]["3"] and gameStats["table"]["1"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["4"] == gameStats["table"]["5"] and gameStats["table"]["5"] == gameStats["table"]["6"] and gameStats["table"]["4"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["7"] == gameStats["table"]["8"] and gameStats["table"]["8"] == gameStats["table"]["9"] and gameStats["table"]["7"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["1"] == gameStats["table"]["4"] and gameStats["table"]["4"] == gameStats["table"]["7"] and gameStats["table"]["1"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["2"] == gameStats["table"]["5"] and gameStats["table"]["5"] == gameStats["table"]["8"] and gameStats["table"]["2"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["3"] == gameStats["table"]["6"] and gameStats["table"]["6"] == gameStats["table"]["9"] and gameStats["table"]["3"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["1"] == gameStats["table"]["5"] and gameStats["table"]["5"] == gameStats["table"]["9"] and gameStats["table"]["1"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()
	elif gameStats["table"]["3"] == gameStats["table"]["5"] and gameStats["table"]["5"] == gameStats["table"]["7"] and gameStats["table"]["3"] != "/":
		if gameStats["currentMove"] == "noughts":
			winner = "Crosses"
		else:
			winner = "Noughts"
		send("Game Over! "+winner+" wins.")
		startGame()

time.sleep(1)
startGame()
while 1:
	gameover()
	output = irc.recv(2040)
	output = output.strip('\n\r')
	sender = output.split(":")[1].split("!")[0]
	try:
		message = output.split(":")[2]
	except:
		print("")
	if message == "PING":
		irc.send("PONG :Pong\n")
	elif message == "help":
		sendPrivateMessage(sender, "Commands:")
		sendPrivateMessage(sender, "help - shows all commands")
		sendPrivateMessage(sender, "game - shows the current game stats including the table")
		sendPrivateMessage(sender, "place 1 crosses - places a cross at place 1 on the table")
		sendPrivateMessage(sender, "place 1 noughts - places a nought at place 1 on the table")
		sendPrivateMessage(sender, "new - starts a new game")
	elif message == "game":
		game(sender)
	elif message.split(" ")[0].strip() == "place":
		spot = message.split(" ")[2]
		team = message.split(" ")[1]
		if gameStats["currentMove"] == team:
			if gameStats["table"][spot] == "/":
				if team == "crosses":
					if sender not in noughts:
						symbol = "x"
						if sender not in crosses:
							global crosses
							crosses.append(sender)
						global gameStats
						gameStats["table"][spot] = symbol
						if gameStats["currentMove"] == "crosses":
							gameStats["currentMove"] = "noughts"
						else:
							gameStats["currentMove"] = "crosses"
						announceGame()
					else:
						sendPrivateMessage(sender, "You can only play in one team per game")
				else:
					if sender not in crosses:
						symbol = "o"
						if sender not in noughts:
							global noughts
							noughts.append(sender)
						global gameStats
						gameStats["table"][spot] = symbol
						if gameStats["currentMove"] == "crosses":
							gameStats["currentMove"] = "noughts"
						else:
							gameStats["currentMove"] = "crosses"
						announceGame()
					else:
						sendPrivateMessage(sender, "You can only play in one team per game")
			else:
				sendPrivateMessage(sender, "That spot has been taken up")
		else:
			sendPrivateMessage(sender, "It is not your team's turn to move")
	elif message == "new":
		startGame()