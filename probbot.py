import os
import praw
import random
import re
import time

# Returns a string containing the results of the dice rolls.
def rollDice(numDice, numSides, addor, no_breakdown) :
	if no_breakdown : numDice = min(numDice, 1000)
	else : numDice = min(numDice, 50)
	numSides = min(numSides, 10000)
	results = []
	for i in range(numDice) :
		results.append(random.randint(1, numSides))
	output = "You rolled " + str(sum(results) + addor*numDice) + "."
	if not no_breakdown and numDice != 1 :
		output += " Breakdown: "
		for result in results[:-1] :
			output += str(result)
			if addor != 0 : output += "+" + str(addor)
			output += ", "
		output += str(results[len(results)-1])
		if addor != 0 : output += "+" + str(addor)
	return output + "\n\n"

# Returns a string containing the results of the coin flips.
def flipCoins(numCoins) :
	numCoins = min(numCoins, 1000)
	results = []
	for i in range(numCoins) :
		results.append(random.randint(0, 1))
	return "You got " + str(results.count(0)) + " heads and " + str(results.count(1)) + " tails.\n\n"
	

# Stores the comments that have already been replied to, so we don't double comment.
if not os.path.isfile("comments_replied_to.txt") : comments_replied_to = []
else :
	with open("comments_replied_to.txt", "r") as file :
		comments_replied_to = file.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

reddit = praw.Reddit("prob-bot")
subreddit = reddit.subreddit("test")

for comment in subreddit.comments(limit=50) :
	if re.search("/u/ProbabilityBot_", comment.body) and comment.id not in comments_replied_to :
		output = ""
		try :
			status = num = sides = addor = 0
			words = comment.body.split()
			print(comment.id, words)
			for word in words :
				if word == "!roll" : 
					if status == 1 or status == 2 : output += rollDice(1, 6, 0, True)
					elif status == 3 : output += flipCoins(1)
					status = 1
				if word == "!roll_nb" : 
					if status == 1 or status == 2 : output += rollDice(1, 6, 0, True)
					elif status == 3 : output += flipCoins(1)
					status = 2
				if word == "!flip" : 
					if status == 1 or status == 2 : output += rollDice(1, 6, 0, True)
					elif status == 3 : output += flipCoins(1)
					status = 3
				if (status == 1 or status == 2) and re.match("\d(d\d)*", word) :
					parts = re.split("d|\+", word)
					if (len(parts) == 1) :
						num = int(parts[0])
						sides = 6
					elif (len(parts) == 2) :
						num = int(parts[0])
						sides = int(parts[1])
					else :
						num = int(parts[0])
						sides = int(parts[1])
						addor = int(parts[2])
					output += rollDice(num, sides, addor, True if status == 2 else False)
					status = num = sides = addor = 0
				if status == 3 and re.match("\d", word) :
					num = int(word)
					output += flipCoins(num)
					status = num = sides = addor = 0
			if status == 1 or status == 2: output += rollDice(1, 6, 0, True)
			elif status == 2 : output += flipCoins(1)
			if output == "" :
				raise Exception("Invalid syntax")
			print("Replied to ", comment.id)
		except :
			output = "I'm sorry, this comment is improperly formatted or contains no commands. You can view the correct format [here]().\n"
			print("Error on", comment.id)
		print(output)
		output += """\n*****\nThis bot was made by Matthew Garrison. You can view its source [here](). You can contact me on 
				[Reddit](https://www.reddit.com/user/matthew_garrison) or [GitHub](https://github.com/matthewgarrison/).\n"""
		comment.reply(output)
		comments_replied_to.append(comment.id)
		with open("comments_replied_to.txt", "w") as file:
			for comment_id in comments_replied_to:
				file.write(comment_id + "\n")
		time.sleep(100)



print("Done")
