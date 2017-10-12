# Reddit Probability Bot

A bot built in Python that performs basic probability tasks, such as rolling dice or flipping coins.

## Usage

You must first call the bot with `/u/ProbabilityBot_`, and then use one of (or multiple) the following commands:

* `!roll`: Rolls a single, six-sided die.

* `!roll AdB`: Rolls a die with `B` sides, `A` times, and returns the total, as well as the breakdown of what you rolled (if more than one die was rolled). `A` is capped at 50 and `B` is capped at 10000.

* `!roll AdB+C`: Rolls a die with `B` sides and adds `C` to the roll, `A` times, and returns the total, as well as the breakdown of what you rolled (if more than one die was rolled). `A` is capped at 50 and `B` is capped at 10000 (`C` has no cap).

* `roll_nb`: The same as `!roll`.

* `!roll_nb AdB`: The same as `!roll AdB`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!roll_nb AdB+C`: The same as `!roll AdB+C`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!flip`: Flips a single coin.

* `!flip N`: Flips `N` coins.

* `!pi`: Approximates PI with 1000 iterations.

* `!pi N`: Approximates PI with `N` iterations (min is 100 iterations and max is 100000).

## Examples

Commenting: 

```
/u/ProbabilityBot_
!roll
!roll 5d6
!roll 12d10+3
!roll_nb
!roll_nb 500d1303
!roll_nb 343d343+434
!flip
!flip 123
```

Would result in a reply of:

```
You rolled 5.
You rolled 21. Breakdown: 6, 4, 5, 2, 4.
You rolled 101. Breakdown: 3+3, 7+3, 7+3, 10+3, 1+3, 5+3, 4+3, 6+3, 7+3, 9+3, 4+3, 2+3.
You rolled 1.
You rolled 317155.
You rolled 205463.
You got 0 heads and 1 tails.
You got 69 heads and 54 tails.
```

## How am I approximating PI?

The probability of two random numbers being coprime is 6/PI^2. Therefore, if we generate N random numbers, count how many of them are coprime, and do a little math, we can approximate PI. Cool, huh?