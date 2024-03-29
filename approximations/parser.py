#!/usr/bin/env python3

import os
import re
import sys
import matplotlib.pyplot as plt

class Approximation:
    conv_layers = []
    top1 = float("NaN")
    top5 = float("NaN")
    time_delta = float("NaN")
    energy_delta = float("NaN")
    def __init__(self, conv_layers=[], top1=float("NaN"), top5=float("NaN"), time_delta=float("NaN"), energy_delta=float("NaN")):
        self.conv_layers = conv_layers
        self.top1 = top1
        self.top5 = top5
        self.time_delta = time_delta
        self.energy_delta = energy_delta

def parse_accuracy(lines):
    accuracy_results = []
    baseline_top1 = float("NaN")
    baseline_top5 = float("NaN")
    i = 0
    while "&" not in lines[i]:
        i += 1
    i += 1
    accuracy_line = [line.strip() for line in lines[i].split("&")]
    (baseline_top1, baseline_top5) = (float(accuracy_line[1]), float(accuracy_line[2]))
    i += 1
    while "&" in lines[i]:
        if lines[i].startswith("%"):
            continue
        accuracy_line = [line.strip() for line in lines[i].split("&")]
        accuracy_layers = [int(layer) for layer in accuracy_line[0].split(",")]
        new_accuracy = Approximation(conv_layers=accuracy_layers, top1=float(accuracy_line[1]), top5=float(accuracy_line[2]), time_delta=float(accuracy_line[3]), energy_delta=float(accuracy_line[4][:-9]))
        accuracy_results.append(new_accuracy)
        i += 1
    return (baseline_top1, baseline_top5, accuracy_results)

if __name__ == "__main__":
    cnns = ["inception_v3", "inception_v4", "inception_resnet_v2", "resnet_v2"]
    lines = {}
    accuracy_results = {}
    baseline_top1 = {}
    baseline_top5 = {}


    for cnn in cnns:
        lines = [line.strip() for line in open(cnn + ".tex", "r")]
        (baseline_top1[cnn], baseline_top5[cnn], accuracy_results[cnn]) = parse_accuracy(lines)

    x = {}
    y = {}

    for cnn in cnns:
        x[cnn] = []
        y[cnn] = []
        for result in accuracy_results[cnn]:
            x[cnn].append(result.energy_delta)
            y[cnn].append(baseline_top1[cnn] - result.top1)

    fig = plt.figure()
    markers = ["x", "^", "+", "s"]
    colors = ["darkred", "darkgreen", "darkblue", "darkgoldenrod"]
    plt.xlabel("Energy gain (J)")
    plt.ylabel("Top 1 accuracy drop (p.p.)")
    right = 1.0
    top = 1.0
    ax = fig.add_subplot()
    for (cnn, marker, color) in zip(cnns, markers, colors):
        ax.scatter(x[cnn], y[cnn], color=color, label=cnn, marker=marker, linewidths=0.1, s=40, zorder=2.0)
        right = max(right, max(x[cnn]))
        top = max(top, max(y[cnn]))
        ax.set_xlim(left=0.0, right=right + 0.1)
        ax.set_ylim(bottom=0.0, top=top + 0.1)
    fig.legend()
    plt.grid(linestyle="dashed", zorder=1.0)
    plt.show()
