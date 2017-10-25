import math
import random

from constant import Constant
from direction import Direction

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
		discard_lowest, dl_count, discard_highest, dh_count, target_direction, target_val, 
		explode_direction, explode_val, reroll_direction, reroll_val) :
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
	# Ensure the explode and reroll values wouldn't le
	if explode_direction == Direction.HIGHER and explode_val <= 1 : 
		explode_val = 2
		output += ( "**Warning:** The explode value you tried to use is too low, and would have let to " +
			"an infinite loop.\n\n" )
	elif explode_direction == Direction.LOWER and explode_val >= num_sides : 
		explode_val = num_sides - 1
		output += ( "**Warning:** The explode value you tried to use is too high, and would have let to " +
			"an infinite loop.\n\n" )
	if reroll_direction == Direction.HIGHER and reroll_val <= 1 : 
		reroll_val = 1
		output += ( "**Warning:** The reroll value you tried to use is too low, and would have let to " +
			"an infinite loop.\n\n" )
	elif reroll_direction == Direction.LOWER and reroll_val >= num_sides : 
		reroll_val = num_sides - 1
		output += ( "**Warning:** The reroll value you tried to use is too high, and would have let to " +
			"an infinite loop.\n\n" )

	# Roll the dice, total the results, and sort if necessary. When exploding/rerolling, the total 
	# number of dice rolled will not exceed MAX_DICE.
	results = []
	rerolled_results = []
	i = j = 0
	while i < num_dice :
		if j >= (MAX_DICE_WITHOUT_BREAKDOWN if no_breakdown else MAX_DICE_WITH_BREAKDOWN) : break
		val = random.randint(1, num_sides)
		if is_target(val, explode_val, explode_direction) : 
			i -= 1
		elif is_target(val, reroll_val, reroll_direction) :
			rerolled_results.append(val)
			i -= 1
		results.append(val)
		i += 1
		j += 1
	if sort : results.sort(reverse=True)
	total = sum(results) - sum(rerolled_results)

	num_dice = len(results) - len(rerolled_results)

	# If we are discarding any dice, we'll create a list of what to discard.
	discarded_lowest_results = []
	discarded_highest_results = []
	if discard_lowest :
		discarded_lowest_results = sorted([x for x in results if x not in rerolled_results], reverse=True)
		for i in range(num_dice - dl_count) : discarded_lowest_results.remove(discarded_lowest_results[0])
		total -= sum(discarded_lowest_results)
	if discard_highest :
		discarded_highest_results = sorted([x for x in results if x not in rerolled_results])
		for i in range(num_dice - dh_count) : discarded_highest_results.remove(discarded_highest_results[0])
		total -= sum(discarded_highest_results)

	average_val = total / (num_dice - dl_count - dh_count)

	# Apply the target flag.
	if target_direction != Direction.NONE :
		total = ( count_elements(results, target_val, target_direction) - count_elements(discarded_lowest_results, 
			target_val, target_direction) - count_elements(discarded_highest_results, target_val, target_direction) )

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
		if not discard_lowest and not discard_highest and target_direction == Direction.NONE :
			for result in results[:-1] : output += str(result) + ", "
			output += str(results[-1])
		else :
			# Check if the current result is being discarded. If so, strike it through and remove 
			# it from the list of discarded rolls.
			for i in range(len(results)) :
				if results[i] in rerolled_results :
					output += "`" + str(results[i]) + "`"
					rerolled_results.remove(results[i])
				elif results[i] in discarded_lowest_results :
					output += "~~" + str(results[i]) + "~~"
					discarded_lowest_results.remove(results[i])
				elif results[i] in discarded_highest_results :
					output += "~~" + str(results[i]) + "~~"
					discarded_highest_results.remove(results[i])
				elif is_target(results[i], target_val, target_direction) :
					output += "**" + str(results[i]) + "**"
				else : output += str(results[i])
				output += (", " if i != len(results)-1 else "")
		output += ")"
		if constant_type == Constant.ADD : output += " + " + str(constant)
		elif constant_type == Constant.SUBTRACT : output += " - " + str(constant)
		elif constant_type == Constant.MULTIPLY : output += " * " + str(constant)
		output += "."
	return output + "\n\n"

def count_elements(list, target_val, direction) :
	count = 0
	for val in list :
		if is_target(val, target_val, direction) : count += 1
	return count

def is_target(val, target_val, direction) :
	if direction == Direction.LOWER and val < target_val : return True
	elif direction == Direction.EQUAL and val == target_val : return True
	elif direction == Direction.HIGHER and val > target_val : return True
	return False

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