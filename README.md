# Galru
[![Build Status](https://travis-ci.org/quadram-institute-bioscience/galru.svg?branch=master)](https://travis-ci.org/quadram-institute-bioscience/galru)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/quadram-institute-bioscience/galru/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/andrewjpage/galru/branch/master/graph/badge.svg)](https://codecov.io/gh/andrewjpage/galru)
[![Docker Pulls](https://img.shields.io/docker/pulls/andrewjpage/galru.svg)](https://hub.docker.com/r/andrewjpage/galru)  

## Contents
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Ubuntu/Debian](#ubuntudebian)
    * [Docker](#docker)
  * [Usage](#usage)
  * [License](#license)
  * [Feedback/Issues](#feedbackissues)
  * [Citation](#citation)

## Introduction
Galru allows you to 

# Installation
If you just want to quickly try out the software please try a Docker continer. This software is designed to run on Linux and OSX. It will not run on Windows.

## Conda
[![Anaconda-Server Badge](https://anaconda.org/bioconda/galru/badges/latest_release_date.svg)](https://anaconda.org/bioconda/galru)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/galru/badges/platforms.svg)](https://anaconda.org/bioconda/galru)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/galru/badges/downloads.svg)](https://anaconda.org/bioconda/galru)

To install Galru, first install [conda with Python3](https://conda.io/en/latest/miniconda.html) then run:

```
conda install -c conda-forge -c bioconda galru
```

## Docker
Install [Docker](https://www.docker.com/).  There is a docker container which gets automatically built from the latest version of Galru. To install it:

```
docker pull andrewjpage/galru
```

To use it you would use a command such as this (substituting in your filename/directories), using the example file in this repository:
```
docker run --rm -it -v /path/to/example_data:/example_data andrewjpage/galru galru xxxxx
```

# Usage

## Quick start


## galru





# License
Galru is free software, licensed under [GPLv3](https://raw.githubusercontent.com/quadram-institute-bioscience/galru/master/VERSION/LICENSE).

# Feedback/Issues
Please report any issues or to provide feedback please go to the [issues page](https://github.com/quadram-institute-bioscience/galru/issues). If you make improvements to the software, add databases or extend profiles, please send us the changes though a [pull request](https://github.com/quadram-institute-bioscience/galru/pulls) so that the whole community may benefit from your work.

# Citation
Coming soon

# Resources required


# Etymology
[galrú](https://www.teanglann.ie/en/fgb/galr%C3%BA) (Gal-roo) is the word for infection in Irish (Gaeilge). 
