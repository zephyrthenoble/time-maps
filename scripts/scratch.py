import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# times: list of datetimes corresponding to each tweet
# times_tot_mins: list giving the time elapsed since midnight for each tweet
# sep_array: array containing xy coordinates of the time map points
times  = np.load("C:\\Users\\Mitchell\\PycharmProjects\\time-maps\\scripts\\times.npy", allow_pickle=True)
times_tot_mins = np.load("C:\\Users\\Mitchell\\PycharmProjects\\time-maps\\scripts\\times_tot_mins.npy", allow_pickle=True)
sep_array = np.load("C:\\Users\\Mitchell\\PycharmProjects\\time-maps\\scripts\\sep_array.npy", allow_pickle=True)
import pandas

print("rendering 3D time map ...")
before = sep_array[:, 0]
after = sep_array[:, 1]
raw_datetimes = times[1:-1]
time_since_midnight = times_tot_mins[1:-1]
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]]
)
scatter = go.Scatter(
    x=before,
    y=after,
    # colors=Zs,
    mode="markers",
)
scatter3d = go.Scatter3d(x=before, y=after, z=times_tot_mins, mode="markers")
fig.add_trace(
    scatter3d,
    row=1, col=1)
fig.add_trace(
    scatter3d,
    row=1, col=2)
fig.show()
