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
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
    #for x, y in zip(xs, ys):
    #    ax.plot(x, y, lw=2)
    ax.plot(xs[0], ys[0], lw=1)
    ax.grid(True)
    ax.set_xlabel(
        x_label,
        fontsize=15,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        y_label,
        fontsize=15,
        fontweight='bold',
        color='black')
    #ax.set_title(
    #    title,
    #    fontsize=18,
    #    fontweight='bold',
    #    color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
    ax.set_xlim(0, 0.1)
    ax.set_ylim(0, 50000)
    if show:
        plt.show()
    plt.savefig(out_path, bbox_inches='tight')
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
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
    #for y in ys:
    #    ax.plot(y, lw=2)
    ax.plot(ys[0], lw=1)
    ax.grid(True)
    ax.set_xlabel(
        x_label,
        fontsize=15,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        y_label,
        fontsize=15,
        fontweight='bold',
        color='black')
    #ax.set_title(
    #    title,
    #    fontsize=18,
    #    fontweight='bold',
    #    color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
    if show:
        plt.show()
    plt.savefig(out_path, bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)
