# Reddit Probability Bot

A bot built in Python that performs basic probability tasks, such as rolling dice or flipping coins. You can view the bot [here](https://www.reddit.com/user/ProbabilityBot_).

## Usage

You must first call the bot with `/u/ProbabilityBot_`, and then use one (or multiple) of the following commands. You can only have one command per line, and it must be at the beginning of the line.

### !roll

This command rolls one or more dice, and provides a breakdown of what you rolled. The maximum number of dice you can roll at once is 50 and the maximum number of sides a given die can have is 10000.

#### Arguments

You can specify how many and what kind of dice to using standard dice notation:

* `X`: rolls `X` 6-sided dice

* `dY`: rolls a single `Y`-sided die

* `XdY`: rolls `X` `Y`-sided dice

* `XdY+Z`: rolls `X` `Y`-sided dice and adds `Z` to the total

* `XdY-Z`: rolls `X` `Y`-sided dice and subtracts `Z` from the total

* `XdY*Z`: rolls `X` `Y`-sided dice and multiplies the total by `Z`

In addition, you can use these flags:

* `--nb`: no breakdown of your rolls is provided and increases the maximum number of dice you can roll at once to 1000

* `--s`: sorts the breakdown of your results (descending)

### !flip 

Flips one or more coins.

#### Arguments 

* `N`: flips `N` coins

### !pi

Approximates pi using 1000 iterations.

#### Arguments

* `N`: use `N` iterations

## Examples

If you commented: 

```
/u/ProbabilityBot_
!roll
!roll 5d7
!roll d10
!roll 12d5+4
!roll 4d2+-5
!roll 6d7-9
!roll 5d87--10
!roll 6d7*2
!roll 25d250 --s
!roll 350d350 --nb
!flip
!flip 40
!pi
!pi 4000
```

You would get a reply like:

```
You rolled 1.
You rolled 17. Breakdown: (4, 1, 5, 4, 3).
You rolled 6.
You rolled 44. Breakdown: (3, 4, 1, 2, 5, 1, 3, 5, 3, 4, 5, 4) + 4.
You rolled 1. Breakdown: (2, 2, 1, 1) + -5.
You rolled 11. Breakdown: (3, 2, 5, 5, 4, 1) - 9.
You rolled 126. Breakdown: (16, 3, 53, 3, 41) - -10.
You rolled 50. Breakdown: (2, 5, 2, 7, 3, 6) * 2.
You rolled 3208. Breakdown: (227, 210, 207, 206, 198, 176, 171, 156, 155, 145, 130, 127, 126, 126, 123, 114, 110, 99, 95, 85, 84, 71, 38, 27, 2).
You got tails.
You got 20 heads and 20 tails.
With 100 iterations, I approximated PI as 3.302891295379082.
With 4000 iterations, I approximated PI as 3.1517891481565017.
```

## How am I approximating PI?

The probability of two random numbers being coprime is 6/π<sup>2</sup> ([source](http://www.cut-the-knot.org/m/Probability/TwoCoprime.shtml)). Therefore, if we generate N pairs of random numbers, count how many of them are coprime, and do a little math, we can approximate PI. Cool, huh?
