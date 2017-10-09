import random

# Returns a list containing the results of the dice rolls.
def rollDice(numDice, numSides) :
	results = []
	for i in range(numDice) :
		results.append(random.randint(1, numSides))
	return results

# Returns a list containing the results of the coin flips (Heads=1 and Tails=2).
def flipCoins(numCoins) :
	results = []
	for i in range(numCoins) :
		results.append(random.randint(0, 1))
	return results

while (True) :
	kind = input("What kind?\n")
	if (kind == "dice") :
		num = int(input("How many?\n"))
		sides = int(input("Sides?\n"))
		addor = input("Plus anything?\n")
		results = rollDice(num, sides)
		print("You rolled", sum(results))
		for result in results :
			if (addor == 0) : print(result, end=", ")
			else : print(result, "+", addor, sep = "", end=", ")
		print()
	elif (kind == "coin") :
		num = int(input("How many?\n"))
		results = flipCoins(num)
		print("You got", results.count(0), "heads and", results.count(1), "tails.")
	else : print("Invalid response. Try again.")