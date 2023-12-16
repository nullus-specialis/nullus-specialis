#!/usr/bin/env python3
# fileSizeDistribution.py
# For a given path graph file size distribution.

import os
import matplotlib.pyplot as plt
from collections import defaultdict
import subprocess

def get_file_sizes(directory):
    file_sizes = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path) / (1024 ** 2)  # Convert bytes to megabytes
            file_sizes[root].append(size)

    return file_sizes

def plot_distribution(file_sizes):
    plt.figure(figsize=(15, 5))

    for file in file_sizes:
	    plt.hist(file_sizes[file], bins=15, alpha=0.8, label=file)

    plt.title('File Size Distribution for directory')
    plt.xlabel('File Size (MB)')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.grid(True)

    plt.savefig('/tmp/dshieldManager.fileSizeDistributionSubs.png')
    plt.show()

def open_with_gpicview(image_path):
    try:
        subprocess.run(['gpicview', image_path])
    except FileNotFoundError:
        print("gpicview is not installed. Please install it or use another image viewer.")

def main():
    directory = input("Enter the directory path: ")

    if not os.path.isdir(directory):
        print("Invalid directory path. Please provide a valid directory.")
        return

    file_sizes = get_file_sizes(directory)
    plot_distribution(file_sizes)

    print("File size distribution graph saved as '/tmp/dshieldManager.fileSizeDistributionSubs.png'")
    open_with_gpicview('/tmp/dshieldManager.fileSizeDistributionSubs.png')

if __name__ == "__main__":
    main()
