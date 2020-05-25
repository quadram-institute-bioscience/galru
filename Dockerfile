FROM continuumio/anaconda3
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge
RUN conda install git pip minimap2 cd-hit bedtools minced samtools ncbi-genome-download blast
RUN pip install git+git://github.com/quadram-institute-bioscience/galru.git

