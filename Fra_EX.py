# -*- coding: utf-8 -*-
"""1160_Lab2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1szmdHZ-hI40SnLkm2tZ4Sye6aldHqI3O
"""

#TASK1

import ffmpeg
import json
import os

input_video = r'../sample.mp4'

def extract_frame_info(input_video):
    try:
        probe = ffmpeg.probe(input_video, select_streams='v', show_frames=None, print_format='json')
        for frame in probe['frames']:
            print(f"Frame Number: {frame.get('coded_picture_number', 'N/A')}")
            print(f"Frame Type: {frame.get('pict_type', 'N/A')}")
            # Use .get() with a default value to handle missing 'pts_time'
            print(f"Timestamp: {frame.get('pts_time', 'N/A')}")
            print(f"Size: {frame.get('pkt_size', 'N/A')} bytes")
            print("-" + "-"*50)

    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")

extract_frame_info(input_video)

#TASK2

import ffmpeg
import json
import os
import matplotlib.pyplot as plt

input_video = r'/sample.mp4'
def extract_frame_info(input_video):
    try:
        probe = ffmpeg.probe(input_video, select_streams='v', show_frames=None, print_format='json')
        frame_counts = {'I': 0, 'P': 0, 'B': 0}
        total_frames = 0
        for frame in probe['frames']:
            frame_type = frame['pict_type']
            if frame_type in frame_counts:
                frame_counts[frame_type] += 1
                total_frames += 1
        percentages = {key: (value / total_frames) * 100 for key, value in frame_counts.items()}
        print(f"I-frames: {frame_counts['I']} ({percentages['I']:.2f}%)")
        print(f"P-frames: {frame_counts['P']} ({percentages['P']:.2f}%)")
        print(f"B-frames: {frame_counts['B']} ({percentages['B']:.2f}%)")
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")
    plot_frame_distribution(frame_counts, percentages)

def plot_frame_distribution(frame_counts, percentages):
    frame_types = list(frame_counts.keys())
    counts = list(frame_counts.values())
    percents = [percentages[key] for key in frame_types]

    # Bar graph
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(frame_types, counts, color=['blue', 'green', 'red'])
    plt.xlabel('Frame Type')
    plt.ylabel('Count')
    plt.title('Frame Count Distribution')

    # Pie chart
    plt.subplot(1, 2, 2)
    plt.pie(percents, labels=frame_types, autopct='%1.1f%%', colors=['blue', 'green', 'red'])
    plt.title('Frame Percentage Distribution')

    # Show plots
    plt.tight_layout()
    plt.show()

extract_frame_info(input_video)

#TASK3

import ffmpeg
import json
from PIL import Image
import os

input_video = r'/sample.mp4'
output_dir = 'extracted_frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_frames(input_video, output_dir):
    try:
        ffmpeg.input(input_video).output(os.path.join(output_dir, 'Iframe_%04d.png'), vf='select=eq(pict_type\\,I)', vsync='vfr').run()
        ffmpeg.input(input_video).output(os.path.join(output_dir, 'Pframe_%04d.png'), vf='select=eq(pict_type\\,P)', vsync='vfr').run()
        ffmpeg.input(input_video).output(os.path.join(output_dir, 'Bframe_%04d.png'), vf='select=eq(pict_type\\,B)', vsync='vfr').run()
        print(f"Frames have been successfully extracted and saved in '{output_dir}'.")

    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")

def display_frames_pillow(output_dir):
    for frame_file in sorted(os.listdir(output_dir)):
        frame_path = os.path.join(output_dir, frame_file)
        img = Image.open(frame_path)
        img.show()

extract_frames(input_video, output_dir)
display_frames_pillow(output_dir)

#TASK4

import ffmpeg
import os

input_dir = 'extracted_frames'

def calculate_frame_sizes(input_dir):
    frame_sizes = {'I': [], 'P': [], 'B': []}

    for frame_file in sorted(os.listdir(input_dir)):
        frame_path = os.path.join(input_dir, frame_file)
        frame_size = os.path.getsize(frame_path)

        # Determine frame type from filename
        if 'I' in frame_file:
            frame_type = 'I'
        elif 'P' in frame_file:
            frame_type = 'P'
        elif 'B' in frame_file:
            frame_type = 'B'
        else:
            continue

        frame_sizes[frame_type].append(frame_size)

    # Calculate average sizes
    average_sizes = {key: (sum(sizes) / len(sizes) if sizes else 0) for key, sizes in frame_sizes.items()}

    # Print results
    print("\nFrame Type Sizes:")
    for frame_type, sizes in frame_sizes.items():
        print(f"Total {frame_type}-frames: {len(sizes)}, Average size: {average_sizes[frame_type]:.2f} bytes")

    # Compare average sizes
    print("\nAverage Size Comparison:")
    for frame_type in average_sizes:
        print(f"{frame_type}-frames: {average_sizes[frame_type]:.2f} bytes")

    return average_sizes

frame_sizes = calculate_frame_sizes(input_dir)

#TASK5

import ffmpeg
import os

input_video = r'/sample.mp4'
output_video = 'reconstructed_video.mp4'
reduced_frame_rate = 1
output_dir = 'extracted_I_frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_frames(input_video, output_dir):
    try:
        ffmpeg.input(input_video).output(os.path.join(output_dir, 'Iframe_%04d.png'), vf='select=eq(pict_type\\,I)', vsync='vfr').run()
        print(f"Frames have been successfully extracted and saved in '{output_dir}'.")

    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")

def create_video_from_frames(frames_dir, output_video, frame_rate):
    try:
        ffmpeg.input(os.path.join(frames_dir, 'frame_%04d.png'), framerate=frame_rate).output(output_video).run()
        print(f"New video created successfully: '{output_video}' with frame rate {frame_rate}.")
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")

extract_frames(input_video, output_dir)
# create_video_from_frames(output_dir, output_video, reduced_frame_rate) # You may want to uncomment this to create a video from frames
