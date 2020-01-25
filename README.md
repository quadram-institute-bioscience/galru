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
Galru is a Python 3 program that defines CRISPR spacer repertoire directly from uncorrected metagenomic long reads.

Galru first identifies long reads that map to CRISPR-associated genes and 
searches along the read for the CRISPR spacer array. This array is compared
 to a database of known arrays to identify the sequence type (MLST).

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

```
usage: galru [options] database uncorrected_long_reads.fastq

Identify CRISPR types from uncorrected long reads

positional arguments:
  species               Species name, use galru_species to see all available
  input_file            Input FASTQ file of uncorrected long reads (optionally
                        gzipped)

optional arguments:
  -h, --help            show this help message and exit
  --db_dir DB_DIR, -d DB_DIR
                        Base directory for species databases, defaults to
                        bundled (default: None)
  --cas_fasta CAS_FASTA, -c CAS_FASTA
                        Cas gene FASTA file (optionally gzipped), defaults to
                        bundled (default: None)
  --technology {map-ont,map-pb,ava-pb,ava-ont}, -y {map-ont,map-pb,ava-pb,ava-ont}
                        Sequencing technology (default: map-ont)
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output filename, defaults to STDOUT (default: None)
  --gene_start_offset GENE_START_OFFSET, -g GENE_START_OFFSET
                        Only count CRISPR reads which cover this base
                        (default: 15)
  --min_mapping_quality MIN_MAPPING_QUALITY, -m MIN_MAPPING_QUALITY
                        Minimum mapping quality score (default: 1)
  --debug               Turn on debugging and save intermediate files
                        (default: False)
  --verbose, -v         Turn on verbose output (default: False)
  --version             show program's version number and exit
```

# Galru create database

```
usage: galru_create_database [options] "species"

Given a species name, create a database

positional arguments:
  species               Species in quotes

optional arguments:
  -h, --help            show this help message and exit
  --output_directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Output directory, defaults to species name in current
                        directory (default: None)
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --refseq_category {all,reference,representative}, -c {all,reference,representative}
                        Sequencing technology (default: all)
  --assembly_level {all,complete,chromosome,scaffold,contig}, -l {all,complete,chromosome,scaffold,contig}
                        Assembly level (default: complete)
  --cdhit_seq_identity CDHIT_SEQ_IDENTITY, -i CDHIT_SEQ_IDENTITY
                        Sequence identity for CD-hit (default: 0.99)
  --allow_missing_st, -a
                        Use files with missing ST [False]
  --debug               Turn on debugging and save intermediate files
                        (default: False)
  --verbose, -v         Turn on verbose output (default: False)
  --version             show program's version number and exit

```

## Galru create species
```
usage: galru_create_database [options] "species"

Given a species name, create a database

positional arguments:
  species               Species in quotes

optional arguments:
  -h, --help            show this help message and exit
  --output_directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Output directory, defaults to species name in current
                        directory (default: None)
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --refseq_category {all,reference,representative}, -c {all,reference,representative}
                        Sequencing technology (default: all)
  --assembly_level {all,complete,chromosome,scaffold,contig}, -l {all,complete,chromosome,scaffold,contig}
                        Assembly level (default: complete)
  --cdhit_seq_identity CDHIT_SEQ_IDENTITY, -i CDHIT_SEQ_IDENTITY
                        Sequence identity for CD-hit (default: 0.99)
  --allow_missing_st, -a
                        Use files with missing ST [False]
  --debug               Turn on debugging and save intermediate files
                        (default: False)
  --verbose, -v         Turn on verbose output (default: False)
  --version             show program's version number and exit
```

## Galru species
```
usage: galru_genera [options]

List all available genera

optional arguments:
  -h, --help     show this help message and exit
  --debug        Turn on debugging and save intermediate files (default:
                 False)
  --verbose, -v  Turn on verbose output (default: False)
  --version      show program's version number and exit
```


# License
Galru is free software, licensed under [GPLv3](https://raw.githubusercontent.com/quadram-institute-bioscience/galru/master/VERSION/LICENSE).

# Feedback/Issues
Please report any issues or to provide feedback please go to the [issues page](https://github.com/quadram-institute-bioscience/galru/issues). If you make improvements to the software, add databases or extend profiles, please send us the changes though a [pull request](https://github.com/quadram-institute-bioscience/galru/pulls) so that the whole community may benefit from your work.

# Citation
Coming soon

# Resources required


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
* mlst (torstens)
* ncbi-genome-download 
* blast+

## Pypi
* fastaq (from pyfastaq)

