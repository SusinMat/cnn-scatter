#!/usr/bin/env python3

import os
import re
import sys
import matplotlib.pyplot as plt

class Layer:
    index = None
    orig_time = float("NaN")
    orig_energy = float("NaN")
    approx_time = float("NaN")
    approx_energy = float("NaN")
    def __init__(self, index = None, orig_time = float("NaN"), orig_energy = float("NaN"), approx_time = float("NaN"), approx_energy = float("NaN")):
        self.index = index
        self.orig_time = orig_time
        self.orig_energy = orig_energy
        self.approx_time = approx_time
        self.approx_energy = approx_energy

def parse_layers(performance_lines, max_performance_lines):
    performance_results = []
    max_performance_results = []
    i = 0
    while "&" not in performance_lines[i]:
        i += 1
    i += 2
    while "&" in performance_lines[i]:
        performance_line = [line.strip() for line in performance_lines[i].split("&")]
        max_performance_line = [line.strip() for line in max_performance_lines[i].split("&")]
        performance_line[-1][:-9]
        new_layer = Layer(index=int(performance_line[0]),
                          orig_time=int(performance_line[1]),
                          orig_energy=float(performance_line[2]),
                          approx_time=float(performance_line[1]) - float(performance_line[3]),
                          approx_energy=float(performance_line[2]) - float(performance_line[4]))
        performance_results.append(new_layer)
        new_layer = Layer(index=int(max_performance_line[0]),
                          orig_time=int(max_performance_line[1]),
                          orig_energy=float(max_performance_line[2]),
                          approx_time=float(max_performance_line[1]) - float(max_performance_line[3]),
                          approx_energy=float(max_performance_line[2]) - float(max_performance_line[4]))
        max_performance_results.append(new_layer)
        i += 1
    return (performance_results, max_performance_results)

if __name__ == "__main__":
    cnns = ["inception_v3", "inception_v4", "squeezenet", "inception_resnet_v2", "resnet_v2"]
    performance_lines = {}
    max_performance_lines = {}
    performance_results = {}
    max_performance_results = {}


    for cnn in cnns:
        performance_lines     = [line.strip() for line in open(cnn + "-performance.tex", "r")]
        max_performance_lines = [line.strip() for line in open(cnn + "-max-performance.tex", "r")]
        (performance_results[cnn], max_performance_results[cnn]) = parse_layers(performance_lines, max_performance_lines)


    for cnn in cnns:
        fig = plt.figure()
        performance_marker = "o"
        performance_color = "darkcyan"
        max_performance_marker = "x"
        max_performance_color = "chocolate"
        plt.xlabel("Original energy (J)")
        plt.ylabel("Approximate (J)")
        ax = fig.add_subplot()
        x = [layer.orig_energy for layer in performance_results[cnn]]
        y = [layer.approx_energy for layer in performance_results[cnn]]
        ax.scatter(x, y, color=performance_color, label="Current implementation", marker=performance_marker, linewidths=0.1, s=40, zorder=2.0)
        x = [layer.orig_energy for layer in max_performance_results[cnn]]
        y = [layer.approx_energy for layer in max_performance_results[cnn]]
        ax.scatter(x, y, color=max_performance_color, label="Upper bound", marker=max_performance_marker, linewidths=0.1, s=40, zorder=2.0)
        fig.legend()
        plt.grid(linestyle="dashed", zorder=1.0)
        plt.show()
