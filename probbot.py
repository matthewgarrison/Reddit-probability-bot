import os
import praw
import random
import re
import sys
import time

# Returns a string containing the results of the dice rolls.
def roll_dice(num_dice, num_sides, addor, no_breakdown) :
	if no_breakdown : num_dice = max(min(num_dice, 1000), 1)
	else : num_dice = max(min(num_dice, 50), 1)
	num_sides = max(min(num_sides, 10000), 2)
	results = []
	for i in range(num_dice) :
		results.append(random.randint(1, num_sides))
	output = "You rolled " + str(sum(results) + addor*num_dice) + "."
	if not no_breakdown and num_dice != 1 :
		output += " Breakdown: "
		for result in results[:-1] :
			output += str(result)
			if addor != 0 : output += "+" + str(addor)
			output += ", "
		output += str(results[len(results)-1])
		if addor != 0 : output += "+" + str(addor)
		output += "."
	return output + "\n\n"

# Returns a string containing the results of the coin flips.
def flip_coins(num_coins) :
	num_coins = max(min(num_coins, 1000), 1)
	results = []
	for i in range(num_coins) :
		results.append(random.randint(0, 1))
	return "You got " + str(results.count(0)) + " heads and " + str(results.count(1)) + " tails.\n\n"
	
RUNNING_ON_HEROKU = False
if len(sys.argv) > 1 :
	if sys.argv[1] == "T" : RUNNING_ON_HEROKU = True

# Stores the comments that have already been replied to, so we don't double comment.
if not os.path.isfile("comments_replied_to.txt") : comments_replied_to = []
else :
	with open("comments_replied_to.txt", "r") as file :
		comments_replied_to = file.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

if RUNNING_ON_HEROKU : reddit = praw.Reddit(username=os.environ["REDDIT_USERNAME"], password=os.environ["REDDIT_PASSWORD"], 
	client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"], user_agent=os.environ["USER_AGENT"])
else : reddit = praw.Reddit("prob-bot")

for comment in reddit.inbox.unread(limit=None) :
	if re.search("/u/ProbabilityBot_", comment.body) and comment.id not in comments_replied_to :
		output = ""
		try :
			lines = comment.body.splitlines()
			for line in lines :
				words = re.split("[^a-zA-Z0-9\!\+_\-]+", line)
				print(comment.id, words)
				i = 0
				while i < len(words)-1 :
					if words[i] == "!roll" or words[i] == "!roll_nb" : 
						no_breakdown = (words[i] == "!roll_nb")
						num = 1
						sides = 6
						addor = 0
						if re.match("\d(d\d)*", words[i+1]) :
							parts = re.split("d|\+", words[i+1])
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
						output += roll_dice(num, sides, addor, no_breakdown)
					if words[i] == "!flip" : 
						num = 1
						if re.match("\d", words[i+1]) : num = int(words[i+1])
						output += flip_coins(num)
					i += 1
				if words[-1] == "!roll" or words[-1] == "!roll_nb" : output += roll_dice(1, 6, 0, True)
				elif words[-1] == "!flip" : output += flip_coins(1)
			if output == "" :
				raise Exception("Invalid syntax")
			print("Replied to ", comment.id)
		except :
			output = """I'm sorry, this comment is improperly formatted or contains no commands. You can view the correct format 
					[here](https://github.com/matthewgarrison/Reddit-probability-bot#usage).\n"""
			print("Error on", comment.id)
		print(output)
		output += """\n*****\nThis bot was made by Matthew Garrison. You can view its source 
				[here](https://github.com/matthewgarrison/Reddit-probability-bot). You can contact me on 
				[Reddit](https://www.reddit.com/user/matthew_garrison) or [GitHub](https://github.com/matthewgarrison/).\n"""
		comment.reply(output)
		comment.mark_read()
		comments_replied_to.append(comment.id)
		with open("comments_replied_to.txt", "w") as file:
			for comment_id in comments_replied_to:
				file.write(comment_id + "\n")
		time.sleep(100)
print("done")


