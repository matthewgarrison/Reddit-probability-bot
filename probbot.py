import os
import re
import sys
import time
import traceback

import praw

from constant import Constant
from direction import Direction
import helper

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
					target_direction = Direction.NONE
					target_val = 0
					no_breakdown = sort = average = False
					explode_val = 0
					explode_direction = Direction.NONE
					reroll_val = 1
					reroll_direction = Direction.NONE
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
						explode_val = num_dice
						while i < len(words) :
							# No breakdown, sort, and average flags.
							if words[i] == "--nb" : no_breakdown = True
							elif words[i] == "--s" : sort = True
							elif words[i] == "--a" : average = True
							# Discard rolls.
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
							# Set a target roll.
							elif words[i] == "--tl" :
								target_direction = Direction.LOWER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									target_val = int(words[i+1])
							elif words[i] == "--te" :
								target_direction = Direction.EQUAL
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									target_val = int(words[i+1])
							elif words[i] == "--th" :
								target_direction = Direction.HIGHER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									target_val = int(words[i+1])
							# Set exploding rolls
							elif words[i] == "--el" :
								explode_direction = Direction.LOWER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									explode_val = int(words[i+1])
							elif words[i] == "--ee" :
								explode_direction = Direction.EQUAL
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									explode_val = int(words[i+1])
							elif words[i] == "--eh" :
								explode_direction = Direction.HIGHER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									explode_val = int(words[i+1])
							# Set a reroll target.
							elif words[i] == "--rl" :
								reroll_direction = Direction.LOWER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									reroll_val = int(words[i+1])
							elif words[i] == "--re" :
								reroll_direction = Direction.EQUAL
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									reroll_val = int(words[i+1])
							elif words[i] == "--rh" :
								reroll_direction = Direction.HIGHER
								if i+1 < len(words) and re.fullmatch("\d+", words[i+1]) : 
									reroll_val = int(words[i+1])
							i += 1
					output += quote(line)
					if discard_lowest or discard_highest :
						discard_total = (dl_count if discard_lowest else 0) + (dh_count if discard_highest else 0)
						if discard_total > num_dice :
							output += ( "**Warning:** You are discarding more dice than you are rolling. This will " +
								"lead to undefined behavior.\n\n" )
					output += ( helper.roll_dice(num_dice, num_sides, constant, constant_type, no_breakdown, 
							sort, average, discard_lowest, dl_count, discard_highest, dh_count, 
							target_direction, target_val, explode_direction, explode_val, reroll_direction, 
							reroll_val) )
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
					output += quote(line) + helper.fate_dice(num_dice, constant, constant_type, no_breakdown)
				elif words[0] == "!flip" :
					num = 1
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += quote(line) + helper.flip_coins(num)
				elif words[0] == "!pi" :
					num = 1000
					if len(words) > 1 and re.fullmatch("\d+", words[1]) : num = int(words[1])
					output += quote(line) + helper.calc_pi(num)
				
				
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


