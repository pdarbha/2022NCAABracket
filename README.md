# 2022NCAABracket
My attempt at submitting a bracket with the greatest expected point value (by weighted CBS rules)

# Motivation

Every year, millions of people participate in March Madness bracket competitions, which involve predicting every game's result in the annual NCAA Basketball National Champtionship tournament.

Each of these games have different structures for rewarding correct predictions. A popular game format that is a favorite of mine is CBS Sports's game mode where for each game pick, a player is rewarded with a point value equal to the product of the rank of the winning team and a multiplier based on the round. This weights predicting an upset over a favorite and later matchups over earlier ones.

# How it Works (At a high level)

This specific bracket game format introduces an interesting twist to the challenge of putting together a bracket. We aren't only trying to predict games based on a specific probability threshold, but we also want to maximize the expected return by weighing the win probability with the expected return from each outcome. 

For example, if #1 Gonzaga has a 94% chance of beating #16 Austin-Peay, traditional probability models will have us choosing Gonzaga to advance. In this game mode, however, the expected value of Gonzaga winning is 0.94 where as the expected value of Austin-Peay is 0.96. Despite the very low probaility of an upset, the reward makes it worth the risk!

Then why not predict upsets at every turn, and make a profit off the few that hit? Well bracket predictions involve not just picking one game, but the results of the matchups that are set by the predicted outcomes. In other words, you lose out on long term gains by going for short term optimization (aka this is very greedy).

Using the same example from above, while it may be worth it to predict an Austin-Peay win, a Gonzaga loss proves to be very expensive as they have a very high probability of advancing another 2-3 rounds. That means we should not only weigh the expected value of that current matchup, but also the expected value we lose out on by picking against each team.

# Implementation Details

To determine the probability of each team beating another team, an SVM with 5-fold validation was trained using [KenPom](https://kenpom.com/) advanced stats that were collected throughout the season. KenPom is the creation of Ken Pomeroy, a very popular college basketball blogger and stat collecter. An SVM was chosen as it's a simple classifier and the feature space is pretty small.

# How to Run It

## Requirements

 * Python3+
 * scikit-learn
 * pandas
 * numpy (should be installed by the above)
 * BeautifulSoup

## Steps

1. scrape-kenpom.py
    This script scrapes KenPom, a popular college basketball advanced stats website, for the advanced stats for each team in the past 20 tournaments. The teams from 2003-2021 get outputted to `final_data.csv` and the 2022 data gets outputted to `2022_data.csv`

2. training-data.py
    This script takes the CSV generated above and creates a training set of every march madness game over the last 20 years based on the teams' KenPom stats. This is outputted to `training_data.csv`

3. generate_probabilities.py
    This script trains an SVM classifier to predict which team will win given 2 teams' KenPom stats. Using this model, it determines the probability of each team in the 2022 field beating the others. This is outputted to `probabilities_2022.csv`

4. generate_538_data.py
    This script takes 538 data which has the probability of each team winning a game in a certain round and makes it more useful by cleaning it up and indexing it to match the order of the other files. This is outputted to `538rounddata.csv`

5. predict_2022.py
    Based on different algorithms, this script takes the probabilites generated earlier and makes bracket predictions.
