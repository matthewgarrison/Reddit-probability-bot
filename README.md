# Reddit Probability Bot

A bot built in Python that performs basic probability tasks, such as rolling dice or flipping coins. You can view the bot [here](https://www.reddit.com/user/ProbabilityBot_).

## Usage

You must first call the bot with `/u/ProbabilityBot_`, and then use one (or multiple) of the following commands. You can only have one command per line, and it must be at the beginning of the line.

### !roll

This command rolls one or more dice, and provides a breakdown of what you rolled. By default, it rolls a single 6-sided die. The maximum number of dice you can roll at once is 50 and the maximum number of sides a given die can have is 10000.

#### Arguments

You can specify how many and what kind of dice to using standard dice notation:

* `X`: rolls `X` 6-sided dice

* `dY`: rolls a single `Y`-sided die

* `XdY`: rolls `X` `Y`-sided dice

* `XdY+Z`: rolls `X` `Y`-sided dice and adds `Z` to the total

* `XdY-Z`: rolls `X` `Y`-sided dice and subtracts `Z` from the total

* `XdY*Z`: rolls `X` `Y`-sided dice and multiplies the total by `Z`

In addition, you can use these flags:

* `--nb`: no breakdown of your rolls is provided and the maximum number of dice you can roll at once is increased to 1000

* `--s`: sorts the breakdown of your rolls (descending)

* `--a`: calculates the average result of your rolls

* `--dl`: discards the lowest roll

* `--dl N`: discards the lowest `N` rolls

* `--dh`: discards the highest roll

* `--dh N`: discards the highest `N` rolls

### !fate

Rolls [Fate](https://en.wikipedia.org/wiki/Fudge_(role-playing_game_system)#Fudge_dice) (or Fudge) dice. By default, it rolls 4 dice.

#### Arguments

You can specify how many kind of dice to using standard dice notation:

* `X`: rolls `X` Fate dice

* `+Y`: rolls 4 Fate dice and adds `Y` to the total

* `-Y`: rolls 4 Fate dice and subtracts `Y` from the total

* `*Y`: rolls 4 Fate dice and multiplies the total by `Y`

* `X+Y`: rolls `X` Fate dice and adds `Y` to the total

* `X-Y`: rolls `X` Fate dice and subtracts `Y` from the total

* `X*Y`: rolls `X` Fate dice and multiplies the total by `Y`

In addition, you can use these flags:

* `--nb`: no breakdown of your rolls is provided and the maximum number of dice you can roll at once is increased to 1000

### !flip 

Flips one or more coins. By default, it flips a single coin.

#### Arguments 

* `N`: flips `N` coins

### !pi

Approximates pi. The probability of two random numbers being coprime is 6/π<sup>2</sup> ([source](http://www.cut-the-knot.org/m/Probability/TwoCoprime.shtml)). Therefore, if we generate N pairs of random numbers, count how many of them are coprime, and do a little math, we can approximate PI. By default, it uses 1000 pairs of random numbers. The maximum number of pairs you can do is 100000.

#### Arguments

* `N`: use `N` pairs of random numbers

## Examples

If you commented: 

```
/u/ProbabilityBot_
!roll
!roll 5d7
!roll d10
!roll 12d5+4
!roll 6d7-9
!roll 6d7*2
!roll 25d250 --s --a
!roll 500d20 --nb --a
!roll 10d20 --dl 5
!roll 10d20 --dh 3
!fate
!fate +3
!fate -2
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
You rolled 11. Breakdown: (3, 2, 5, 5, 4, 1) - 9.
You rolled 50. Breakdown: (2, 5, 2, 7, 3, 6) * 2.
You rolled 115, with an average of 9.5833. Breakdown: (20, 18, 17, 14, 13, 8, 7, 6, 5, 5, 1, 1).
You rolled 4827, with an average of 9.6540.
You rolled 81. Breakdown: (~~2~~, ~~8~~, ~~7~~, 15, 16, ~~11~~, 20, ~~1~~, 11, 19).
You rolled 51. Breakdown: (12, ~~16~~, 13, 2, 2, 10, ~~18~~, ~~15~~, 4, 8).
You rolled -1. Breakdown: (0, 0, -, 0).
You rolled 3. Breakdown: (-, 0, +, 0) + 3.
You rolled -1. Breakdown: (+, 0, -, +) - 2.
You got tails.
You got 20 heads and 20 tails.
With 1000 iterations, I approximated PI as 3.194383.
With 4000 iterations, I approximated PI as 3.140759.
```

