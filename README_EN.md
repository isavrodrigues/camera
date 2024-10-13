# camera

A simple hello world module

If you are going to *develop* from this repository, go to the [development guide](README_DEV.md).

## Installing camera:

Remember to follow these instructions from within your preferred virtual environment:

    conda create -n camera python=True
    conda activate camera

The first way is to clone the repository and do a local installation:

    git clone https://github.com/isavrodrigues/camera.git
    cd camera
    pip install .

The second way is to install directly:

    pip install git+https://github.com/isavrodrigues/camera.git

To uninstall, use:

    pip uninstall camera

## Usage

To find all implemented commands, run:

    camera-cli --help
