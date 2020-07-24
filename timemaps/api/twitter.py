import datetime as dt
from os import path
import numpy as np
from twython import Twython

import matplotlib.pylab as plt

import timemaps


def analyze_tweet_times(name_to_get, all_tweets, HEAT, save_location="./", title=""):
    # plots a heated or normal time map, and return lists of time quantities
    # input:
    # name_to_get: twitter handle, not including @
    # all tweets: list of tweets. Each tweet is a neted dictionary
    # HEAT: Boolean; 1 for a heated time map, 0 for a normal scatterplot
    #
    # output:
    # times: list of datetimes corresponding to each tweet
    # times_tot_mins: list giving the time elapsed since midnight for each tweet
    # sep_array: array containing xy coordinates of the time map points

    assert path.exists(save_location)
    assert path.isdir(save_location)
    if save_location.endswith("/"):
        save_location = save_location[:-1]

    if title == "":
        title = name_to_get

    all_tweets = all_tweets[
        ::-1
    ]  # reverse order so that most recent tweets are at the end

    times = [get_dt(tweet["created_at"]) for tweet in all_tweets]
    timezone_shift = dt.timedelta(hours=4)  # times are in GMT. Convert to eastern time.
    times = [time - timezone_shift for time in times]

    times_tot_mins = 24 * 60 - (
        60 * np.array([t.hour for t in times]) + np.array([t.minute for t in times])
    )  # 24*60 - number of minutes since midnight

    seps = np.array(
        [(times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))]
    )
    seps[seps == 0] = 1  # convert zero second separations to 1-second separations

    sep_array = np.zeros(
        (len(seps) - 1, 2)
    )  # 1st column: x-coords, 2nd column: y-coords
    sep_array[:, 0] = seps[:-1]
    sep_array[:, 1] = seps[1:]

    if HEAT == 0:
        Ncolors = 24 * 60  # a different shade for each minute
        timemaps.make_time_map(times, times_tot_mins, sep_array, Ncolors, title)
    if HEAT == 1:
        Nside = 4 * 256  # number of pixels along the x and y directions
        width = 4  # the number of pixels that specifies the width of the Gaussians for the Gaussian filter
        timemaps.make_heated_time_map(sep_array, Nside, width, title)
    if HEAT == 2:
        Ncolors = 24 * 60  # a different shade for each minute
        timemaps.make_3d_time_map(times, times_tot_mins, sep_array, Ncolors, title)

    print("writing file...")
    print(
        "To avoid cluttered labels, you may have to expand the plotting window by dragging, and then save the figure"
    )
    print(
        'to save as an eps, type: plt.savefig("filename.eps", format="eps",bbox_inches="tight", dpi=200)'
    )
    print("Done!")

    plt.savefig(
        f"{save_location}/{name_to_get}.png", format="png", bbox_inches="tight", dpi=200
    )  # save as svg

    return times, times_tot_mins, sep_array


def twitter_auth2(app_key, app_secret):  # for Twython authentication

    twitter = Twython(app_key, app_secret, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    twitter = Twython(app_key, access_token=ACCESS_TOKEN)

    return twitter


def get_dt(t):  # converts a twitter time string to a datetime object

    splitted = t.split(" ")
    new_string = " ".join(splitted[:4]) + " " + splitted[-1]
    my_datetime = dt.datetime.strptime(new_string, "%c")

    return my_datetime


def grab_tweets(
    name_to_get, app_key, app_secret
):  # download a user's twitter timeline, returning a list of tweets

    print("downloading tweets:")

    twitter = twitter_auth2(app_key, app_secret)
    first = twitter.get_user_timeline(screen_name=name_to_get, count=1)

    lis = [first[0]["id"]]  # list of tweet id's

    all_tweets = []

    N_packets = 16  # since packets come with 200 tweets each, this will add up to 3,200 (the maximum amount)

    for i in range(N_packets):

        print("tweet packet =", i + 1)
        user_timeline = twitter.get_user_timeline(
            screen_name=name_to_get, count=200, max_id=lis[-1] - 1
        )
        # if max_id=lis[-1], the earliest tweet from the last packet will be included as well

        all_tweets += user_timeline

        if i == 0:
            lis = [tweet["id"] for tweet in user_timeline]
        else:
            lis += [tweet["id"] for tweet in user_timeline]

    tweet_ids = [tweet["id"] for tweet in all_tweets]
    print("number of unique tweets:", len(set(tweet_ids)))

    return all_tweets
