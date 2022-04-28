
"""

Set of functions to find breaks in error metric in video
Visualize KPI in order to help us define the values

"""


import matplotlib.pyplot as plt

def metric(flabels):
    """
    metric for discontinuity analysis
    """
    tp = len(flabels['tp'])
    fn = len(flabels['fn'])
    fp = len(flabels['fp'])

    if (tp + fn + fp) == 0:
        return 1

    else:
        return tp/(tp + fn + fp)

def avg_kpi(flabels, attribute, types = None):
    """
    types: tp, fp, fn
    if types == None, we consider all types of images
    """
    kpi = 0
    num = 0
    if types == None:
        types = flabels.keys()
    for type in types:
        for i in range(len(flabels)):
            kpi += flabels[type][i][attribute]
            num +=1

    if num != 0:
        return kpi/num
    else:
        return 0

def max_kpi(flabels, attribute, types = None):
    kpi = float('n')
    if types == None:
        types = flabels.keys()
    for type in types:
        for i in range(len(flabels)):
            if kpi < flabels[type][i][attribute]:
                kpi = flabels[type][i][attribute]

    return kpi

def min_kpi(flabels, attribute, types = None):
    kpi = float('-inf')
    if types == None:
        types = flabels.keys()
    for type in types:
        for i in range(len(flabels)):
            if kpi > flabels[type][i][attribute]:
                kpi = flabels[type][i][attribute]
    return kpi

def find_breaks(labels, metric, arange = 5, max_min = 0, diff = 0.5):
    breaks = {}
    total = arange*2 + max_min
    for video in labels:
        frame = total
        breaks[video] = []
        while frame < len(labels[video]):
            start_frame = frame - total
            start_metric = 0
            for i in range(arange):
                start_metric += metric[video][start_frame + i]
            start_metric = start_metric/arange
        
            end_metric = 0
            for i in range(arange):
                end_metric += metric[video][start_frame + arange + max_min + i]
            end_metric = end_metric/arange

            if abs(end_metric - start_metric) > diff:
                breaks[video].append(start_frame)
                frame += total
            else:
                frame += 1

    return breaks

def display_kpi(labels, video, total, arange, max_min, start_frame, kpi_funct):
    end_frame = start_frame + total
    Y = []
    for i in range(start_frame, end_frame, 1):
        kpi = kpi_funct(labels[video][i])
        Y.append(kpi)
    plt.scatter(list(range(len(Y))), Y)
    plt.axvline(x=arange)
    plt.axvline(x=(arange + max_min))