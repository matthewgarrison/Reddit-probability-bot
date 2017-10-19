# Reddit Probability Bot

A bot built in Python that performs basic probability tasks, such as rolling dice or flipping coins. You can view the bot [here](https://www.reddit.com/user/ProbabilityBot_).

## Usage

You must first call the bot with `/u/ProbabilityBot_`, and then use one (or multiple) of the following commands:

* `!roll`: Rolls a single, six-sided die.

* `!roll AdB`: Rolls a die with `B` sides, `A` times, and returns the total, as well as the breakdown of what you rolled (if more than one die was rolled). `A` is capped at 50 and `B` is capped at 10000.

* `!roll AdB+C`: Rolls a die with `B` sides and adds `C` to the roll, `A` times, and returns the total, as well as the breakdown of what you rolled (if more than one die was rolled). `A` is capped at 50 and `B` is capped at 10000 (`C` has no cap, and can be negative).

* `roll_nb`: The same as `!roll`.

* `!roll_nb AdB`: The same as `!roll AdB`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!roll_nb AdB+C`: The same as `!roll AdB+C`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!flip`: Flips a single coin.

* `!flip N`: Flips `N` coins.

* `!pi`: Approximates PI with 1000 iterations.

* `!pi N`: Approximates PI with `N` iterations (min is 100 iterations and max is 100000).

## Examples

If you commented: 

```
/u/ProbabilityBot_
!roll
!roll 12
!roll 7d8
!roll 4d9+10
!roll 6d4+-2
!roll_nb
!roll_nb 15
!roll_nb 9d4
!roll_nb 15d5+6
!roll_nb 12d6+-3
!flip
!flip 20
!pi
!pi 12345
```

You would get a reply like:

```
You rolled 3.
You rolled 50. Breakdown: 4, 4, 1, 6, 6, 1, 6, 6, 2, 5, 5, 4.
You rolled 41. Breakdown: 6, 6, 5, 8, 6, 2, 8.
You rolled 52. Breakdown: 8+10, 1+10, 1+10, 2+10.
You rolled 2. Breakdown: 2+-2, 1+-2, 3+-2, 3+-2, 3+-2, 2+-2.
You rolled 6.
You rolled 67.
You rolled 17.
You rolled 134.
You rolled 2.
You got heads.
You got 10 heads and 10 tails.
With 1000 iterations, I approximated PI as 3.1570203370643455.
With 12345 iterations, I approximated PI as 3.1472297068205846.
```

## How am I approximating PI?

The probability of two random numbers being coprime is 6/π<sup>2</sup> ([source](http://www.cut-the-knot.org/m/Probability/TwoCoprime.shtml)). Therefore, if we generate N pairs of random numbers, count how many of them are coprime, and do a little math, we can approximate PI. Cool, huh?
