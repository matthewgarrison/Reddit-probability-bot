import math
import os
import praw
import random
import re
import sys
import time
import traceback
from enum import Enum

class Constant(Enum) :
	NONE = 0
	ADD = 1
	SUBTRACT = 2
	MULTIPLY = 3

class Discard(Enum) :
	NONE = 0
	LOWEST = 1
	HIGHEST = 2


# Returns a string containing the results of the dice rolls.
def roll_dice(num_dice, num_sides, constant, constant_type, no_breakdown, sort, average, discard_count, discard_type) :
	if no_breakdown : num_dice = max(min(num_dice, 1000), 1)
	else : num_dice = max(min(num_dice, 50), 1)
	num_sides = max(min(num_sides, 10000), 2)
	results = []
	for i in range(num_dice) :
		results.append(random.randint(1, num_sides))
	if sort : results.sort(reverse=True)
	total = sum(results)
	if discard_type != Discard.NONE :
		# Sort the list then remove all the dice we are keeping.
		if discard_type == Discard.LOWEST : discarded_results = sorted(results, reverse=True)
		else : discarded_results = sorted(results)
		for i in range(num_dice - discard_count) : discarded_results.remove(discarded_results[0])
		total -= sum(discarded_results)
	if constant_type == Constant.ADD : total += constant
	elif constant_type == Constant.SUBTRACT : total -= constant
	elif constant_type == Constant.MULTIPLY : total *= constant
	output = "You rolled " + str(total)
	if average : output += ", with an average of " + "{:.4f}".format(total / num_dice)
	output += "."
	if not no_breakdown and num_dice != 1 :
		output += " Breakdown: ("
		if discard_type == Discard.NONE :
			for result in results[:-1] : output += str(result) + ", "
			output += str(results[-1])
		else :
			for result in results[:-1] :
				if result in discarded_results :
					output += "~~" + str(result) + "~~" + ", "
					discarded_results.remove(result)
				else : output += str(result) + ", "
			if results[-1] in discarded_results :
				output += "~~" + str(results[-1]) + "~~"
				discarded_results.remove(results[-1])
			else : output += str(results[-1])
		output += ")"
		if constant_type == Constant.ADD : output += " + " + str(constant)
		elif constant_type == Constant.SUBTRACT : output += " - " + str(constant)
		elif constant_type == Constant.MULTIPLY : output += " * " + str(constant)
		output += "."
	return output + "\n\n"

# Returns a string containing the results of the dice rolls.
def fate_dice(num_dice, constant, constant_type, no_breakdown) :
	if no_breakdown : num_dice = max(min(num_dice, 1000), 1)
	else : num_dice = max(min(num_dice, 50), 1)
	results = []
	for i in range(num_dice) :
		results.append(random.randint(-1, 1))
	total = sum(results)
	if constant_type == Constant.ADD : total += constant
	elif constant_type == Constant.SUBTRACT : total -= constant
	elif constant_type == Constant.MULTIPLY : total *= constant
	output = "You rolled " + str(total) + "."
	if not no_breakdown and num_dice != 1 :
		output += " Breakdown: ("
		for result in results[:-1] : output += fate_format(result) + ", "
		output += fate_format(results[-1])
		output += ")"
		if constant_type == Constant.ADD : output += " + " + str(constant)
		elif constant_type == Constant.SUBTRACT : output += " - " + str(constant)
		elif constant_type == Constant.MULTIPLY : output += " * " + str(constant)
		output += "."
	return output + "\n\n"

# Formats the fate dice rolls.
def fate_format(result) :
	if result == -1 : return "-"
	elif result == 1 : return "+"
	else : return "0"

# Returns a string containing the results of the coin flips.
def flip_coins(num_coins) :
	num_coins = max(min(num_coins, 1000), 1)
	results = []
	for i in range(num_coins) :
		results.append(random.randint(0, 1))
	if num_coins == 1 :
		ans = ("heads" if results[0] == 0 else "tails")
		return "You got " + ans + ".\n\n"
	else : return "You got " + str(results.count(0)) + " heads and " + str(results.count(1)) + " tails.\n\n"
	
# Approximates PI using the fact that the probability of two random numbers being comprime is 6/PI^2.
# Source: http://www.cut-the-knot.org/m/Probability/TwoCoprime.shtml
def calc_pi(num_iterations) :
	num_iterations = max(min(num_iterations, 100000), 100)
	num_coprime = 0
	for i in range(num_iterations) :
		one = random.randrange(10000000)
		two = random.randrange(10000000)
		if GCD(one, two) == 1 : num_coprime += 1
	prob_comprime = num_coprime / num_iterations
	pi = math.sqrt(6 / prob_comprime)
	return "With " + str(num_iterations) + " iterations, I approximated PI as " + "{:f}".format(pi) + ".\n\n"

# Calcualtes the GCD of two numbers (using the Euclidean Algorithm).
def GCD(a, b) :
	return a if b == 0 else GCD(b, a % b)





# Pass in "T" as a CLI argument to indicate that this script is running on Heroku.
RUNNING_ON_HEROKU = False
if len(sys.argv) > 1 :
	if sys.argv[1] == "T" : RUNNING_ON_HEROKU = True

if RUNNING_ON_HEROKU : reddit = praw.Reddit(username=os.environ["REDDIT_USERNAME"], 
	password=os.environ["REDDIT_PASSWORD"], client_id=os.environ["CLIENT_ID"], 
	client_secret=os.environ["CLIENT_SECRET"], user_agent=os.environ["USER_AGENT"])
else : reddit = praw.Reddit("prob-bot")

# Subreddits that do not like bots, that this bot will not comment in.
with open("banned_subreddits.txt", "r") as file :
	banned_subreddits = file.read()
	banned_subreddits = banned_subreddits.split("\n")
	banned_subreddits = list(filter(None, banned_subreddits))

for comment in reddit.inbox.unread(limit=None) :
	subreddit = str(comment.subreddit)
	if subreddit in banned_subreddits :
		comment.mark_read()
		continue
	if re.search("/u/ProbabilityBot_", comment.body, re.IGNORECASE) :
		output = ""
		try :
			lines = comment.body.splitlines()
			for line in lines :
				words = re.split("\s+", line)
				print(comment.id, words)
				if words[0] == "!roll" :
					num_dice = 1
					num_sides = 0
					constant = 0
					constant_type = Constant.NONE
					discard_count = 1
					discard_type = Discard.NONE
					no_breakdown = sort = average = False
					if len(words) > 1 :
						if re.fullmatch("\d+", words[1]) : 
							# A
							num_dice = int(words[1])
						elif re.fullmatch("d\d+", words[1]) : 
							# dB
							num_sides = int(words[1][1:])
						elif re.fullmatch("\d+d\d+", words[1]) :
							# AdB
							parts = words[1].split("d")
							num_dice = int(parts[0])
							num_sides = int(parts[1])
						match = re.fullmatch("\d+d\d+(\+|-|\*)-?\d+", words[1])
						if match :
							# AdB(+|-|*)C 
							parts = re.split("[d+\-*]", words[1], maxsplit=2)
							num_dice = int(parts[0])
							num_sides = int(parts[1])
							constant = int(parts[2])
							if match.group(1) == "+" : constant_type = Constant.ADD
							elif match.group(1) == "-" : constant_type = Constant.SUBTRACT
							elif match.group(1) == "*" : constant_type = Constant.MULTIPLY
						i = 1
						while i < len(words) :
							if words[i] == "--nb" : no_breakdown = True
							elif words[i] == "--s" : sort = True
							elif words[i] == "--a" : average = True
							elif words[i] == "--dl" :
								discard_type = Discard.LOWEST
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									discard_count = int(words[i+1])
							elif words[i] == "--dh" :
								discard_type = Discard.HIGHEST
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									discard_count = int(words[i+1])
							i += 1
					output += ( roll_dice(num_dice, num_sides, constant, constant_type, no_breakdown, 
						sort, average, discard_count, discard_type) )
				elif words[0] == "!fate" :
					num_dice = 4
					constant = 0
					constant_type = Constant.NONE
					no_breakdown = False
					if len(words) > 1 :
						if re.fullmatch("\d+", words[1]) : 
							# A
							num_dice = int(words[1])
						match = re.fullmatch("\d+(\+|-|\*)-?\d+", words[1])
						if match :
							# A(+|-|*)B
							parts = re.split("[d+\-*]", words[1], maxsplit=2)
							num_dice = int(parts[0])
							constant = int(parts[1])
							if match.group(1) == "+" : constant_type = Constant.ADD
							elif match.group(1) == "-" : constant_type = Constant.SUBTRACT
							elif match.group(1) == "*" : constant_type = Constant.MULTIPLY
						match = re.fullmatch("(\+|-|\*)-?\d+", words[1])
						if match :
							# (+|-|*)B
							parts = re.split("[+\-*]", words[1], maxsplit=1)
							constant = int(parts[1])
							if match.group(1) == "+" : constant_type = Constant.ADD
							elif match.group(1) == "-" : constant_type = Constant.SUBTRACT
							elif match.group(1) == "*" : constant_type = Constant.MULTIPLY
						i = 1
						while i < len(words) :
							if words[i] == "--nb" : no_breakdown = True
							i += 1
					output += fate_dice(num_dice, constant, constant_type, no_breakdown)
				elif words[0] == "!flip" :
					num = 1
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += flip_coins(num)
				elif words[0] == "!pi" :
					num = 1000
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += calc_pi(num)
				
				
			if output == "" :
				raise Exception("Invalid syntax")
			print("Replied to", comment.id)
		except :
			output = ( "I'm sorry, this comment is improperly formatted or contains no commands. You can " +
					"view the correct format [here](https://github.com/matthewgarrison/Reddit-probability-bot#usage).\n\n" )
			print("Error on", comment.id)
			traceback.print_exc()
		print(output)
		github = ("GitHub" if RUNNING_ON_HEROKU else "Github")
		output += ( "*****\n\n^^made ^^by ^^Matthew ^^Garrison ^^| [^^source ^^code]" +
				"(https://github.com/matthewgarrison/Reddit-probability-bot) ^^| ^^contact ^^me ^^on " +
				"[^^Reddit](https://www.reddit.com/user/matthew_garrison) ^^or [^^" + github + 
				"](https://github.com/matthewgarrison/)\n\n" )
		comment.reply(output)
		comment.mark_read()
		time.sleep(20)
print("done")


