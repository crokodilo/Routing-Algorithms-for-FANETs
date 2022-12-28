import matplotlib.pyplot as plt
import json
import numpy as np
import matplotlib
from src.utilities import config


from argparse import ArgumentParser

LABEL_SIZE = 16

def mean_std_of_metric(filename_format: str, ndrones : int,
                        alg : str, seeds : list, metric : str):
    data = []
    for seed in seeds:
        file_name = filename_format.format(seed, ndrones, alg)
        with open(file_name, 'r') as fp:
            data.append(json.load(fp)[metric])
    return np.mean(data), np.std(data)

def plot_ndrones(filename_format: list, ndrones: list, metric: str,
                 algorithms: list, seeds: list, out_dir: str):
    """ plot for varying ndrones """

    x = list(ndrones)
    y = {}
    # for each algortihm
    for alg in algorithms:
        data_alg = []
        # for each x ticks
        for nd in ndrones:
            data_alg.append(mean_std_of_metric(filename_format, nd, alg, seeds, metric)[0])

        y[alg] = data_alg


    print(x)
    print(y)
    ax = plt.subplot(111)
    fig = plt.gcf()  # get current figure
    fig.set_size_inches(16, 10)

    ax.grid()
    for alg in algorithms:
        ax.plot(x, y[alg], label=alg)

    plt.ylabel(metric, fontsize=LABEL_SIZE)
    plt.xlabel("n drones", fontsize=LABEL_SIZE)

    plt.xticks(ndrones)

    plt.title(metric)

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(labels=algorithms)  # handles, labels, prop={'size': LEGEND_SIZE})
    # plt.tight_layout()
    plt.savefig(out_dir + metric + ".png")
    # plt.show()
    plt.clf()




if __name__ == "__main__":
    #set_font()

    parser = ArgumentParser()


    # MANDATORY
    parser.add_argument("-nd", dest='number_of_drones', action="append", type=int,
                        help="the number of drones to use in the simulataion")
    parser.add_argument("-i_s", dest='initial_seed', action="store", type=int,
                        help="the initial seed to use in the simualtions")
    parser.add_argument("-e_s", dest='end_seed', action="store", type=int,
                        help="the end seed to use in the simualtions"
                             + "-notice that the simulations will run for seed in (i_s, e_s)")
    parser.add_argument("-metric", dest='metric', action="store", type=str,
                        help="the metric to plot")
    parser.add_argument("-alg", dest='algorithms', action="append", type=str,
                        help="the algorithm to plot")

    args = parser.parse_args()
    assert args.metric in ["number_of_events_to_depot", "number_of_packets_to_depot", "packet_mean_delivery_time", "event_mean_delivery_time", "packet_delivery_ratio"]
    pattern_file = config.EXPERIMENTS_DIR + "out__{}_{}_RoutingAlgorithm.{}.json"
    out_dir = config.SAVE_PLOT_DIR
    plot_ndrones(pattern_file, args.number_of_drones, args.metric, args.algorithms, list(range(args.initial_seed, args.end_seed)), out_dir)


