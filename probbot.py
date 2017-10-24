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

MIN_DICE = 1
MIN_SIDES = 2
MAX_DICE_WITH_BREAKDOWN = 50
MAX_DICE_WITHOUT_BREAKDOWN = 1000
MAX_SIDES = 10000
MIN_COINS = 1
MAX_COINS = 1000
MIN_PAIRS = 100
MAX_PAIRS = 100000
CALC_PI_RAND_MAX = 10000000

# Returns a string containing the results of the dice rolls.
def roll_dice(num_dice, num_sides, constant, constant_type, no_breakdown, sort, average, 
		discard_lowest, dl_count, discard_highest, dh_count) :
	output = ""
	# Ensure num_dice and num_sides are within the valid range of values, and output a warning otherwise.
	if no_breakdown : 
		if num_dice > MAX_DICE_WITHOUT_BREAKDOWN or num_dice < MIN_DICE :
			num_dice = max(min(num_dice, MAX_DICE_WITHOUT_BREAKDOWN), MIN_DICE)
			output += ( "**Warning:** The number of dice you tried to roll is outside the range of [" + 
					str(MIN_DICE) + ", " + str(MAX_DICE_WITHOUT_BREAKDOWN) + "].\n\n" )
	else :
		if num_dice > MAX_DICE_WITH_BREAKDOWN or num_dice < MIN_DICE :
			num_dice = max(min(num_dice, MAX_DICE_WITH_BREAKDOWN), MIN_DICE)
			output += ( "**Warning:** The number of dice you tried to roll is outside the range of [" + 
					str(MIN_DICE) + ", " + str(MAX_DICE_WITH_BREAKDOWN) + "].\n\n" )
	if num_sides > MAX_SIDES or num_sides < MIN_SIDES :
		num_sides = max(min(num_sides, MAX_SIDES), MIN_SIDES)
		output += ( "**Warning:** The number of sides you tried to use is outside the range of [" + 
					str(MIN_SIDES) + ", " + str(MAX_SIDES) + "].\n\n" )

	# Roll the dice, total the results, and sort if necessary.
	results = []
	for i in range(num_dice) :
		results.append(random.randint(1, num_sides))
	if sort : results.sort(reverse=True)
	total = sum(results)

	# If we are discarding any dice, we'll create a list of what to discard.
	discarded_lowest_results = []
	discarded_highest_results = []
	if discard_lowest :
		discarded_lowest_results = sorted(results, reverse=True)
		for i in range(num_dice - dl_count) : discarded_lowest_results.remove(discarded_lowest_results[0])
		total -= sum(discarded_lowest_results)
	if discard_highest :
		discarded_highest_results = sorted(results)
		for i in range(num_dice - dh_count) : discarded_highest_results.remove(discarded_highest_results[0])
		total -= sum(discarded_highest_results)

	average_val = total / (num_dice - dl_count - dh_count)

	# Apply the constant, if there is one.
	if constant_type == Constant.ADD : total += constant
	elif constant_type == Constant.SUBTRACT : total -= constant
	elif constant_type == Constant.MULTIPLY : total *= constant

	# Create the output string.
	output += "You rolled " + str(total)
	if average : output += ", with an average of " + "{:.4f}".format(average_val)
	output += "."
	if not no_breakdown and num_dice != 1 :
		output += " Breakdown: ("
		if not discard_lowest and not discard_highest :
			for result in results[:-1] : output += str(result) + ", "
			output += str(results[-1])
		else :
			# Check if the current result is being discarded. If so, strike it through and remove 
			# it from the list of discarded rolls.
			for i in range(num_dice) :
				if results[i] in discarded_lowest_results :
					output += "~~" + str(results[i]) + "~~" + (", " if i != num_dice-1 else "")
					discarded_lowest_results.remove(results[i])
				elif results[i] in discarded_highest_results :
					output += "~~" + str(results[i]) + "~~" + (", " if i != num_dice-1 else "")
					discarded_highest_results.remove(results[i])
				else : output += str(results[i]) + (", " if i != num_dice-1 else "")
		output += ")"
		if constant_type == Constant.ADD : output += " + " + str(constant)
		elif constant_type == Constant.SUBTRACT : output += " - " + str(constant)
		elif constant_type == Constant.MULTIPLY : output += " * " + str(constant)
		output += "."
	return output + "\n\n"

# Returns a string containing the results of the dice rolls.
def fate_dice(num_dice, constant, constant_type, no_breakdown) :
	output = ""
	# Ensure num_dice is within the valid range of values, and output a warning otherwise.
	if no_breakdown : 
		if num_dice > MAX_DICE_WITHOUT_BREAKDOWN or num_dice < MIN_DICE :
			num_dice = max(min(num_dice, MAX_DICE_WITHOUT_BREAKDOWN), MIN_DICE)
			output += ( "**Warning:** The number of dice you tried to roll is outside the range of [" + 
					str(MIN_DICE) + ", " + str(MAX_DICE_WITHOUT_BREAKDOWN) + "].\n\n" )
	else :
		if num_dice > MAX_DICE_WITH_BREAKDOWN or num_dice < MIN_DICE :
			num_dice = max(min(num_dice, MAX_DICE_WITH_BREAKDOWN), MIN_DICE)
			output += ( "**Warning:** The number of dice you tried to roll is outside the range of [" + 
					str(MIN_DICE) + ", " + str(MAX_DICE_WITH_BREAKDOWN) + "].\n\n" )

	# Roll the dice and total the results.
	results = []
	for i in range(num_dice) :
		results.append(random.randint(-1, 1))
	total = sum(results)

	# Apply the constant, if there is one.
	if constant_type == Constant.ADD : total += constant
	elif constant_type == Constant.SUBTRACT : total -= constant
	elif constant_type == Constant.MULTIPLY : total *= constant

	# Create the output string.
	output += "You rolled " + str(total) + "."
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

# Formats the Fate dice rolls.
def fate_format(result) :
	if result == -1 : return "-"
	elif result == 1 : return "+"
	else : return "0"

# Returns a string containing the results of the coin flips.
def flip_coins(num_coins) :
	output = ""
	# Ensure num_coins is within the valid range of values, and output a warning otherwise.
	if num_coins > MAX_COINS or num_coins < MIN_COINS :
		num_coins = max(min(num_coins, MAX_COINS), MIN_COINS)
		output += ( "**Warning:** The number of coins you tried to use is outside the range of [" + 
					str(MIN_COINS) + ", " + str(MAX_COINS) + "].\n\n" )
	
	results = []
	for i in range(num_coins) :
		results.append(random.randint(0, 1))
	if num_coins == 1 :
		ans = ("heads" if results[0] == 0 else "tails")
		output += "You got " + ans + ".\n\n"
	else : output += "You got " + str(results.count(0)) + " heads and " + str(results.count(1)) + " tails.\n\n"
	return output
	
# Approximates PI using the fact that the probability of two random numbers being comprime is 6/PI^2.
# Source: http://www.cut-the-knot.org/m/Probability/TwoCoprime.shtml
def calc_pi(num_pairs) :
	output = ""
	# Ensure num_pairs is within the valid range of values, and output a warning otherwise.
	if num_pairs > MAX_PAIRS or num_pairs < MIN_PAIRS :
		num_pairs = max(min(num_pairs, MAX_PAIRS), MIN_PAIRS)
		output += ( "**Warning:** The number of pairs you tried to use is outside the range of [" + 
					str(MIN_PAIRS) + ", " + str(MAX_PAIRS) + "].\n\n" )
	
	num_coprime = 0
	for i in range(num_pairs) :
		one = random.randrange(CALC_PI_RAND_MAX)
		two = random.randrange(CALC_PI_RAND_MAX)
		if GCD(one, two) == 1 : num_coprime += 1
	prob_comprime = num_coprime / num_pairs
	pi = math.sqrt(6 / prob_comprime)
	output += "With " + str(num_pairs) + " pairs, I approximated PI as " + "{:f}".format(pi) + ".\n\n"
	return output

# Calcualtes the GCD of two numbers (using the Euclidean Algorithm).
def GCD(a, b) :
	return a if b == 0 else GCD(b, a % b)

# Quotes the input, using markdown.
def quote(input) :
	return "> " + input + "\n\n"



# Pass in "T" as a CLI argument to indicate that this script is running on Heroku.
RUNNING_ON_HEROKU = False
if len(sys.argv) > 1 :
	if sys.argv[1] == "T" : RUNNING_ON_HEROKU = True

if RUNNING_ON_HEROKU : reddit = praw.Reddit(username=os.environ["REDDIT_USERNAME"], 
	password=os.environ["REDDIT_PASSWORD"], client_id=os.environ["CLIENT_ID"], 
	client_secret=os.environ["CLIENT_SECRET"], user_agent=os.environ["USER_AGENT"])
else : reddit = praw.Reddit("prob-bot")

# Subreddits that do not like bots, that this bot will not comment in.
with open("anti_bot_subreddits.txt", "r") as file :
	anti_bot_subreddits = file.read()
	anti_bot_subreddits = anti_bot_subreddits.split("\n")
	anti_bot_subreddits = list(filter(None, anti_bot_subreddits))

for comment in reddit.inbox.unread(limit=None) :
	# Ignore the comment if it is in one of the banned subreddits.
	subreddit = str(comment.subreddit)
	if subreddit in anti_bot_subreddits :
		comment.mark_read()
		continue

	if re.search("/u/ProbabilityBot_", comment.body, re.IGNORECASE) :
		output = ""
		try :
			lines = comment.body.splitlines()
			for line in lines :
				words = re.split("\s+", line)
				# This allows you to summon the bot and perform a single command, in one line.
				if re.fullmatch("/u/ProbabilityBot_", words[0], re.IGNORECASE) : del words[0]
				print(comment.id, words)
				if len(words) == 0 : continue;
				if words[0] == "!roll" :
					num_dice = 1
					num_sides = 6
					constant = 0
					constant_type = Constant.NONE
					dh_count = dl_count = 0
					discard_highest = discard_lowest = False
					no_breakdown = sort = average = False
					if len(words) > 1 :
						if re.fullmatch("\d+", words[1]) : 
							# X
							num_dice = int(words[1])

						elif re.fullmatch("d\d+", words[1]) : 
							# dY
							num_sides = int(words[1][1:])
						elif re.fullmatch("\d+d\d+", words[1]) :
							# XdY
							parts = words[1].split("d")
							num_dice = int(parts[0])
							num_sides = int(parts[1])
						match = re.fullmatch("\d+d\d+(\+|-|\*)-?\d+", words[1])
						if match :
							# XdY(+|-|*)Z 
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
								discard_lowest = True
								dl_count = 1
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									dl_count = int(words[i+1])
							elif words[i] == "--dh" :
								discard_highest = True
								dh_count = 1
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									dh_count = int(words[i+1])
							i += 1
					output += quote(line)
					if discard_lowest or discard_highest :
						discard_total = (dl_count if discard_lowest else 0) + (dh_count if discard_highest else 0)
						if discard_total > num_dice :
							output += "**Warning:** You are discarding more dice than you are rolling.\n\n"
					output += ( roll_dice(num_dice, num_sides, constant, constant_type, no_breakdown, 
							sort, average, discard_lowest, dl_count, discard_highest, dh_count) )
				elif words[0] == "!fate" :
					num_dice = 4
					constant = 0
					constant_type = Constant.NONE
					no_breakdown = False
					if len(words) > 1 :
						if re.fullmatch("\d+", words[1]) : 
							# X
							num_dice = int(words[1])
						match = re.fullmatch("\d+(\+|-|\*)-?\d+", words[1])
						if match :
							# X(+|-|*)Y
							parts = re.split("[d+\-*]", words[1], maxsplit=2)
							num_dice = int(parts[0])
							constant = int(parts[1])
							if match.group(1) == "+" : constant_type = Constant.ADD
							elif match.group(1) == "-" : constant_type = Constant.SUBTRACT
							elif match.group(1) == "*" : constant_type = Constant.MULTIPLY
						match = re.fullmatch("(\+|-|\*)-?\d+", words[1])
						if match :
							# (+|-|*)Y
							parts = re.split("[+\-*]", words[1], maxsplit=1)
							constant = int(parts[1])
							if match.group(1) == "+" : constant_type = Constant.ADD
							elif match.group(1) == "-" : constant_type = Constant.SUBTRACT
							elif match.group(1) == "*" : constant_type = Constant.MULTIPLY
						i = 1
						while i < len(words) :
							if words[i] == "--nb" : no_breakdown = True
							i += 1
					output += quote(line) + fate_dice(num_dice, constant, constant_type, no_breakdown)
				elif words[0] == "!flip" :
					num = 1
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += quote(line) + flip_coins(num)
				elif words[0] == "!pi" :
					num = 1000
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += quote(line) + calc_pi(num)
				
				
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


