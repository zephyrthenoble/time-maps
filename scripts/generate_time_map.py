import click
import time_maps

SCATTER=0
HEAT=1

def my_secrets():  # store your twitter codes

    d = {}
    d["APP_KEY"] = "O17AbV1eqmbnbPFv0r9yjLzEL"
    d["APP_SECRET"] = "SJiMvks1mwGqbX1PSkhQWRV5FQXqxhrcoBRaHy5H26eEdq9wS8"
    d["my_access_token_key"] = "807227574-CPr89uEHp1EKI7mcaSwdLdhFXAZ1W0kVhRSP48ZA"
    d["my_access_token_secret"] = "0PywOTj0wHVB84OjqPN5XS9NBUJy4yyNRrstzfsHjNcjO"

    return d


@click.command()
@click.option("--handle","-h", multiple=True)
@click.option("--handle-file","-f", type=click.File())
@click.option("--map-type", "-m", type=click.Choice(["heatmap", "scatter", "both"]), default="scatter")
@click.option("--save-path", type=click.Path(exists=True), default=".")
@click.option("--app-key", required=True)
@click.option("--app-secret", required=True)
#  @click.option("--access-key", required=True)
#  @click.option("--access-secret", required=True)
def generate_time_map(
    handle, handle_file, map_type, save_path, app_key, app_secret
    #  handle, handle_file, map_type, save_path, app_key, app_secret, access_key, access_secret
):
    if not handle and not handle_file:
        raise TypeError("Must pass either a single --handle-file with mutiple handles")

    handles = []
    if handle:
        for h in handle:
            handles.append(h)
    for handle in handle_file:
        handles.append(handle)

    for handle in handles:
        print(f"tweets from {handle}")
        all_tweets = time_maps.tm_tools.grab_tweets(handle, app_key, app_secret)
        if map_type is "scatter" or map_type is "both":
            times, times_tot_mins, sep_array = time_maps.tm_tools.generate(handle, all_tweets, SCATTER, save_path)
        if map_type is "heatmap" or map_type is "both":
            times, times_tot_mins, sep_array = time_maps.tm_tools.generate(handle, all_tweets, HEAT, save_path)





if __name__ == "__main__":
    generate_time_map(auto_envvar_prefix='TIME_MAP')
