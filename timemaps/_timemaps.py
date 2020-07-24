import numpy as np
import matplotlib.pylab as plt
import pandas as pandas
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndi
from colour import Color
from numpy.core._multiarray_umath import ndarray


def make_heated_time_map(
    sep_array, Nside, width, title=""
):  # plot heated time map. Nothing is returned

    print("generating heated time map ...")

    # choose points within specified range. Example plot separations greater than 5 minutes:
    # 	indices = (sep_array[:,0]>5*60) & (sep_array[:,1]>5*60)
    indices = list(range(sep_array.shape[0]))  # all time separations

    x_pts = np.log(sep_array[indices, 0])
    y_pts = np.log(sep_array[indices, 1])

    min_val = np.min([np.min(x_pts), np.min(y_pts)])

    x_pts = x_pts - min_val
    y_pts = y_pts - min_val

    max_val = np.max([np.max(x_pts), np.max(y_pts)])

    x_pts *= (Nside - 1) / max_val
    y_pts *= (Nside - 1) / max_val

    img = np.zeros((Nside, Nside))

    for i in range(len(x_pts)):
        #  print(i)
        #  print((int)x_pts[i])
        #  print(y_pts[i])
        img[(int)(x_pts[i]), (int)(y_pts[i])] += 1

    img = ndi.gaussian_filter(img, width)  # apply Gaussian filter
    img = np.sqrt(img)  # taking the square root makes the lower values more visible
    img = np.transpose(img)  # needed so the orientation is the same as scatterplot

    plt.imshow(img, origin="lower")

    ## create custom tick marks. Calculate positions of tick marks on the transformed log scale of the image array
    plt.minorticks_off()

    ## change font, which can also now accept latex: http://matplotlib.org/users/usetex.html
    plt.rc("text", usetex=False)
    plt.rc("font", family="serif")

    my_max = np.max([np.max(sep_array[indices, 0]), np.max(sep_array[indices, 1])])
    my_min = np.max([np.min(sep_array[indices, 0]), np.min(sep_array[indices, 1])])

    pure_ticks = np.array(
        [1e-3, 1, 10, 60 * 10, 2 * 3600, 1 * 24 * 3600, 7 * 24 * 3600]
    )
    # where the tick marks will be placed, in units of seconds. An additional value will be appended to the end for the max
    labels = [
        "1 ms",
        "1 s",
        "10 s",
        "10 m",
        "2 h",
        "1 d",
        "1 w",
    ]  # tick labels

    index_lower = np.min(np.nonzero(pure_ticks >= my_min))
    # index of minimum tick that is greater than or equal to the smallest time interval. This will be the first tick with a non-blank label

    index_upper = np.max(np.nonzero(pure_ticks <= my_max))
    # similar to index_lower, but for upperbound

    ticks = pure_ticks[index_lower : index_upper + 1]
    ticks = np.log(
        np.hstack((my_min, ticks, my_max))
    )  # append values to beginning and end in order to specify the limits
    ticks = ticks - min_val
    ticks *= (Nside - 1) / (max_val)

    labels = np.hstack(
        ("", labels[index_lower : index_upper + 1], "")
    )  # append blank labels to beginning and end
    plt.xticks(ticks, labels, fontsize=16)
    plt.yticks(ticks, labels, fontsize=16)
    plt.xlabel("Time Before Tweet", fontsize=18)
    plt.ylabel("Time After Tweet", fontsize=18)
    plt.title(title)
    plt.show()

    return None


def make_time_map(
    times, times_tot_mins, sep_array, Ncolors, title
):  # plot standard, scatter-plot time map. Nothing is returned

    print("rendering normal time map ...")

    ## set up color list
    red = Color("red")
    blue = Color("blue")
    color_list = list(
        red.range_to(blue, Ncolors)
    )  # range of colors evenly speced on the spectrum between red and blue. Each element is a colour object
    color_list = [c.hex for c in color_list]  # give hex version

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.rc("text", usetex=False)
    plt.rc("font", family="serif")

    colormap = plt.cm.get_cmap(
        "rainbow"
    )  # see color maps at http://matplotlib.org/users/colormaps.html

    order = np.argsort(times_tot_mins[1:-1])  # so that the red dots are on top
    # 	order=np.arange(1,len(times_tot_mins)-2) # dots are unsorted

    sc = ax.scatter(
        sep_array[:, 0][order],
        sep_array[:, 1][order],
        c=times_tot_mins[1:-1][order],
        vmin=0,
        vmax=24 * 60,
        s=25,
        cmap=colormap,
        marker="o",
        edgecolors="none",
    )
    # taken from http://stackoverflow.com/questions/6063876/matplotlib-colorbar-for-scatter

    color_bar = fig.colorbar(
        sc,
        ticks=[0, 24 * 15, 24 * 30, 24 * 45, 24 * 60],
        orientation="horizontal",
        shrink=0.5,
    )
    color_bar.ax.set_xticklabels(["Midnight", "18:00", "Noon", "6:00", "Midnight"])
    color_bar.ax.invert_xaxis()
    color_bar.ax.tick_params(labelsize=16)

    ax.set_yscale("log")  # logarithmic axes
    ax.set_xscale("log")

    plt.minorticks_off()
    pure_ticks = np.array(
        [1e-3, 1, 10, 60 * 10, 2 * 3600, 1 * 24 * 3600, 7 * 24 * 3600]
    )  # where the tick marks will be placed, in units of seconds.
    labels = [
        "1 ms",
        "1 s",
        "10 s",
        "10 m",
        "2 h",
        "1 d",
        "1 w",
    ]  # tick labels

    max_val = np.max([np.max(sep_array[:, 0]), np.max(sep_array[:, 1])])

    ticks = np.hstack((pure_ticks, max_val))

    min_val = np.min([np.min(sep_array[:, 0]), np.min(sep_array[:, 1])])

    plt.xticks(ticks, labels, fontsize=16)
    plt.yticks(ticks, labels, fontsize=16)

    plt.xlabel("Time Before Tweet", fontsize=18)
    plt.ylabel("Time After Tweet", fontsize=18)
    plt.title(title)

    plt.xlim((min_val, max_val))
    plt.ylim((min_val, max_val))

    ax.set_aspect("equal")
    plt.tight_layout()

    plt.show()


# def make_3d_time_map(
#         times, times_tot_mins, sep_array, Ncolors, title
# ):  # plot standard, scatter-plot time map. Nothing is returned
#
#     print("rendering 3D time map ...")
#
#     ## set up color list
#     red = Color("red")
#     blue = Color("blue")
#     color_list = list(
#         red.range_to(blue, Ncolors+1)
#     )  # range of colors evenly speced on the spectrum between red and blue. Each element is a colour object
#     color_list = [c.hex for c in color_list]  # give hex version
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#
#     plt.rc("text", usetex=False)
#     plt.rc("font", family="serif")
#
#     colormap = plt.cm.get_cmap(
#         "rainbow"
#     )  # see color maps at http://matplotlib.org/users/colormaps.html
#
#     #order = np.argsort(times_tot_mins[1:-1])  # so that the red dots are on top
#     order: ndarray=np.arange(1,len(times_tot_mins)-2) # dots are unsorted
#     # Xs = sep_array[:, 0][order],
#     # Ys = sep_array[:, 1][order],
#     # Zs = tuple(60 * t.hour + t.minute for t in times[1:-1])
#     Xs = np.log10(sep_array[:, 0])
#     Ys = np.log10(sep_array[:, 1])
#     Zs = [float((60 * t.hour) + t.minute) / 60.0 for t in times[1:-1]]
#
#     with open("xs.txt", "w") as f:
#         for e in Xs:
#             f.write(str(e) + "\n")
#     with open("ys.txt", "w") as f:
#         for e in Ys:
#             f.write(str(e)+"\n")
#     with open("zs.txt", "w") as f:
#         for e in Zs:
#             f.write(str(e) + "\n")
#     xsize = len(Xs)
#     ysize = len(Ys)
#     zsize = len(Zs)
#     sc = ax.scatter(
#         Xs,
#         Ys,
#         Zs,
#         # c=times_tot_mins[1:-1],
#         # vmin=0,
#         # vmax=24 * 60,
#         # s=25,
#         # cmap=colormap,
#         # marker="o",
#         # edgecolors="none",
#     )
#     # taken from http://stackoverflow.com/questions/6063876/matplotlib-colorbar-for-scatter
#
#     # color_bar = fig.colorbar(
#     #     sc,
#     #     ticks=[0, 24 * 15, 24 * 30, 24 * 45, 24 * 60],
#     #     orientation="horizontal",
#     #     shrink=0.5,
#     # )
#     # color_bar.ax.set_xticklabels(["Midnight", "18:00", "Noon", "6:00", "Midnight"])
#     # color_bar.ax.invert_xaxis()
#     # color_bar.ax.tick_params(labelsize=16)
#     #
#     # ax.set_yscale("log")  # logarithmic axes
#     # ax.set_xscale("log")
#
#     plt.minorticks_off()
#     pure_ticks = np.log10(np.array(
#         [1e-3, 1, 10, 60 * 10, 2 * 3600, 1 * 24 * 3600, 7 * 24 * 3600]
#     ))  # where the tick marks will be placed, in units of seconds.
#     labels = [
#         "1 ms",
#         "1 s",
#         "10 s",
#         "10 m",
#         "2 h",
#         "1 d",
#         "1 w",
#     ]  # tick labels
#
#     max_val = np.max([np.max(Xs), np.max(Ys)])
#
#     ticks = np.hstack((pure_ticks, max_val))
#
#     min_val = np.min([np.min(Xs), np.min(Ys)])
#
#     plt.xticks(ticks, labels, fontsize=16)
#     plt.yticks(ticks, labels, fontsize=16)
#
#     ax.set_xlabel("Time Before Tweet", fontsize=18)
#     ax.set_ylabel("Time After Tweet", fontsize=18)
#     ax.set_zlabel("Time", fontsize=18)
#     plt.title(title)
#
#     plt.xlim((min_val, max_val))
#     plt.ylim((min_val, max_val))
#
#     plt.show()
def make_3d_time_map(
    times, times_tot_mins, sep_array, Ncolors, title
):  # plot standard, scatter-plot time map. Nothing is returned


    # import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    print("rendering 3D time map ...")
    np.save("sep_array", sep_array)
    np.save("times_tot_mins", times_tot_mins)
    np.save("times", times)
    import sys
    sys.exit()
    df = pandas.DataFrame()
    Xs = sep_array[:, 0]
    Ys = sep_array[:, 1]
    # Zs = times[1:-1]
    Zs = times_tot_mins[1:-1]

    df["before"] = Xs
    df["after"] = Ys
    df["time"] = Zs
    df["colors"] = times[1:-1]
    # df["colors"] = times_tot_mins[1:-1]

    print("plotting")
    # fig = make_subplots(
    #     rows=1, cols=2, specs=[[dict(is_3d=False, type="scatter3d"), dict(is_3d=True, type="scatter3d"),],]
    # )
    fig = make_subplots(
        rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]]
    )
    scatter = go.Scatter(
        x=Xs,
        y=Ys,
        # colors=Zs,
        mode="markers",
    )
    scatter3d = go.Scatter3d(x=Xs, y=Ys, z=Zs, mode="markers",)
    fig.add_trace(
        scatter3d,
        row=1, col=1)
    fig.add_trace(
        scatter3d,
        row=1, col=2)
    fig.show()
