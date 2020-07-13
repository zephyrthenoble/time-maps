#! /usr/local/bin/python  -*- coding: UTF-8 -*-

import csv
import tm_tools

## specify a twitter username and whether you want a heated time map or a normal time map
## an eps file will be saved with the same name as the twitter username
## the axes are automatically scaled logarithmically.


def main():
    with open("twitter_handles.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in csvreader:
            name, handle = row
            print(name, handle)
            HEAT = 1  # 1: get a heated time map
            # 0: get a normal time map, aka scatter plot

            ## download tweets
            all_tweets = tm_tools.grab_tweets(handle)

            ## create plot
            times, times_tot_mins, sep_array = tm_tools.analyze_tweet_times(
                name, all_tweets, HEAT, save_location="/mnt/m/Documents/projs/"
            )


if __name__ == "__main__":
    main()
