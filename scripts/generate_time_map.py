import click
import timemaps
import timemaps.api.twitter

SCATTER = 0
HEAT = 1
THREE_D = 2


@click.command()
@click.option("--handle", "-h", multiple=True)
@click.option("--handle-file", "-f", type=click.File())
@click.option(
    "--map-type",
    "-m",
    type=click.Choice(["heatmap", "scatter", "3D", "all"]),
    default="scatter",
)
@click.option("--save-path", type=click.Path(exists=True), default=".")
@click.option("--app-key", required=True)
@click.option("--app-secret", required=True)
#  @click.option("--access-key", required=True)
#  @click.option("--access-secret", required=True)
def generate_time_map(handle, handle_file, map_type, save_path, app_key, app_secret):
    if not handle and not handle_file:
        raise TypeError("Must pass either a single --handle-file with mutiple handles")

    handles = []
    if handle:
        for h in handle:
            handles.append(h)
    if handle_file:
        for handle in handle_file:
            handles.append(handle)

    for handle in handles:
        print(f"tweets from {handle}")
        all_tweets = timemaps.api.twitter.grab_tweets(handle, app_key, app_secret)
        if map_type is "scatter" or map_type is "all":
            times, times_tot_mins, sep_array = timemaps.api.twitter.analyze_tweet_times(
                handle, all_tweets, SCATTER, save_path
            )
        if map_type is "heatmap" or map_type is "all":
            times, times_tot_mins, sep_array = timemaps.api.twitter.analyze_tweet_times(
                handle, all_tweets, HEAT, save_path
            )
        if map_type is "3D" or map_type is "all":
            times, times_tot_mins, sep_array = timemaps.api.twitter.analyze_tweet_times(
                handle, all_tweets, THREE_D, save_path
            )


def main():
    generate_time_map(auto_envvar_prefix="TIME_MAP")


if __name__ == "__main__":
    main()
