# BPFTracer

A Python-based tool for easy kernel debugging using bpftrace scripts. This tool provides a simple interface to capture and analyze kernel-level information using eBPF technology.

## Prerequisites

- Python 3.6+
- bpftrace
- Linux kernel with eBPF support

## Installation

1. Install bpftrace if not already installed:
```bash
sudo apt-get update
sudo apt-get install -y bpftrace
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
sudo ./bpftracer.py
```

## Features

- Capture kernel version information
- Easy to extend with custom bpftrace scripts
- Simple command-line interface

## Project Structure

```
.
├── bpftracer.py         # Main script
├── scripts/             # Directory for bpftrace scripts
│   └── kernel_info.bt   # Sample bpftrace script
└── README.md           # This file
└── requirements.txt    # Python dependencies
``` 