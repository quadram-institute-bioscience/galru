# Galru
[![Build Status](https://travis-ci.org/quadram-institute-bioscience/galru.svg?branch=master)](https://travis-ci.org/quadram-institute-bioscience/galru)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/quadram-institute-bioscience/galru/blob/master/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/andrewjpage/galru.svg)](https://hub.docker.com/r/quadraminstitute/galru)  

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
Galru allows for rapid spoligotyping for Mycobacterium tuberculosis directly from long read sequencing. It is fast and accurate. It requires a minimal amount of information to produce a spoligotype, and allows for near real-time typing when used to process sequencing data as it is produced by a Nanopore sequencer. 


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
docker pull quadraminstitute/galru
```

To use it you would use a command such as this (substituting in your filename/directories), using the example file in this repository:
```
docker run --rm -it -v /path/to/example_data:/example_data quadraminstitute/galru galru /example_data/example_reads.fastq
```

## Pypi/pip
This is the most difficult installation method and assumes you know how to install dependancies yourself.  Install the dependancies, as listed below.  Then install galru
```
pip install galru
```

To install the development version:
```
pip install git+https://github.com/quadram-institute-bioscience/galru.git
```


# Usage
To run the software provide a FASTQ or FASTA file of reads. This can also be an assembly. Short reads will not work.
```
galru example_reads.fastq
```
This will output a spoligotype in the format
```
1001111111111111111111111111000010110001111
```
where 1 indicates the spacer is present and 0 indicates it is absent.
	

## galru

```
usage: galru [options] uncorrected_long_reads.fastq

Spoligotyping from uncorrected long reads

positional arguments:
  input_file            Input FASTQ file of uncorrected long reads (optionally gzipped)

optional arguments:
  -h, --help            show this help message and exit
  --db_dir DB_DIR, -d DB_DIR
                        Base directory for species databases, defaults to bundled (default: None)
  --cas_fasta CAS_FASTA, -c CAS_FASTA
                        Cas gene FASTA file (optionally gzipped), defaults to bundled (default: None)
  --technology {map-ont,map-pb,ava-pb,ava-ont}, -y {map-ont,map-pb,ava-pb,ava-ont}
                        Sequencing technology (default: map-ont)
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output filename, defaults to STDOUT (default: None)
  --extended_results, -x
                        Output extended results (default: False)
  --gene_start_offset GENE_START_OFFSET, -g GENE_START_OFFSET
                        Only count CRISPR reads which cover this base (default: 30)
  --min_mapping_quality MIN_MAPPING_QUALITY, -m MIN_MAPPING_QUALITY
                        Minimum mapping quality score (default: 10)
  --qcov_margin QCOV_MARGIN, -q QCOV_MARGIN
                        Maximum perc coverage difference between CRISPR and read (default: 100)
  --min_bitscore MIN_BITSCORE, -b MIN_BITSCORE
                        Minimum blast bitscore (default: 38)
  --min_identity MIN_IDENTITY, -i MIN_IDENTITY
                        Minimum blast identity (default: 95)
  --species SPECIES, -s SPECIES
                        Species name, use galru_species to see all available (default: Mycobacterium_tuberculosis)
  --debug               Turn on debugging and save intermediate files (default: False)
  --verbose, -v         Turn on verbose output (default: False)
  --version             show program's version number and exit
```


# License
Galru is free software, licensed under [GPLv3](https://raw.githubusercontent.com/quadram-institute-bioscience/galru/master/VERSION/LICENSE).

# Feedback/Issues
Please report any issues or to provide feedback please go to the [issues page](https://github.com/quadram-institute-bioscience/galru/issues). If you make improvements to the software, add databases or extend profiles, please send us the changes though a [pull request](https://github.com/quadram-institute-bioscience/galru/pulls) so that the whole community may benefit from your work.

# Citation
"Rapid Mycobacterium tuberculosis spoligotyping from uncorrected long reads using Galru", Andrew J. Page, Nabil-Fareed Alikhan, Michael Strinden, Thanh Le Viet, Timofey Skvortsov, 2020.

# Etymology
[galrú](https://www.teanglann.ie/en/fgb/galr%C3%BA) (Gal-roo) is the word for infection in Irish (Gaeilge). 

# External Dependencies
## System
* grep
* xargs
* find 
* gunzip

## Conda
* cd-hit-est (from cd-hit)
* minced
* bedtools
* samtools (1.3 or above)
* minimap2
* ncbi-genome-download 
* blast+
* mlst

## Pypi
* fastaq (from pyfastaq)

