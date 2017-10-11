# Reddit-probability-bot

A bot built in Python that performs basic probability tasks, such as rolling dice or flipping coins.

## Usage

You must first call the bot with `/u/ProbabilityBot_`, and then use one of (or multiple) following commands:

* `!roll`: Rolls a single, six-sided die.

* `!roll AdB`: Rolls a die with `B` sides, `A` times, and returns the total, as well as the breakdown of what you rolled. `A` is capped at 50 and `B` is capped at 10000.

* `!roll AdB+C`: Rolls a die with `B` sides and adds `C` to the roll, `A` times, and returns the total, as well as the breakdown of what you rolled. `A` is capped at 50 and `B` is capped at 10000 (`C` has no cap).

* `!roll_nb AdB`: The same as `!roll AdB`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!roll_nb AdB+C`: The same as `!roll AdB+C`, except no breakdown of your rolls is provided and `A` is capped at 1000.

* `!flip`: Flips a single coin.

* `!flip N` Flips `N` coins.