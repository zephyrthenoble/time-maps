#! /usr/local/bin/python  -*- coding: UTF-8 -*-

import tm_tools

## specify a twitter username and whether you want a heated time map or a normal time map
## an eps file will be saved with the same name as the twitter username
## the axes are automatically scaled logarithmically.
import sys


name_to_get = sys.argv[1]
HEAT = int(sys.argv[2])
# 0: get a normal time map, aka scatter plot

## download tweets
all_tweets = tm_tools.grab_tweets(name_to_get)

## create plot
times, times_tot_mins, sep_array = tm_tools.analyze_tweet_times(
    name_to_get, all_tweets, HEAT
)
