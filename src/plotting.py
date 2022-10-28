import matplotlib.pyplot as plt


def multi_xsys_plot(xs,
                    ys,
                    x_label,
                    y_label,
                    title,
                    out_path,
                    show=False):
    '''
    Plot multiple x, y arrays on the same axis.
    Args:
        xs: <array> contains x-data arrays, same length as ys
        ys: <array> contains y-data arrays, same length as xs
        x_label: <string> x data label (for axis)
        y_label: <string> y data label (for axis)
        title: <string> axis title
        out_path: <string> path to save figure
        show: <bool> if true, figure shows, always saves
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[10, 7])
    for x, y in zip(xs, ys):
        ax.plot(x, y, lw=2)
    ax.grid(True)
    ax.set_xlabel(
        x_label,
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        y_label,
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_title(
        title,
        fontsize=18,
        fontweight='bold',
        color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=14)
    if show:
        plt.show()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)


def multiy_plot(ys,
                x_label,
                y_label,
                title,
                out_path,
                show=False):
    '''
    Plot multiple y arrays on the same axis.
    Args:
        ys: <array> contains y-data arrays, same length as xs
        x_label: <string> x data label (for axis)
        y_label: <string> y data label (for axis)
        title: <string> axis title
        out_path: <string> path to save figure
        show: <bool> if true, figure shows, always saves
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[10, 7])
    for y in ys:
        ax.plot(y, lw=2)
    ax.grid(True)
    ax.set_xlabel(
        x_label,
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        y_label,
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_title(
        title,
        fontsize=18,
        fontweight='bold',
        color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=14)
    if show:
        plt.show()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)
