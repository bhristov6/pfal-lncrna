# iMARGI

The paper describing the iMARGI-seq protocol is here [paper](https://www.biorxiv.org/content/10.1101/681924v1.full.pdf). I ran manually the scripts instead of the Docker container provided by the paper's authors. 


I downloaded the data iMARGI data Trevor sent me (total of 5 pair-end experiments) into [~proj/Data/LeRochLab/iMARGI](~proj/Data/LeRochLab/iMARGI). Working on getting the scripts to run bug free. 

## Basic statistics.

| experiment | total reads | cleaned | % |  mapped | % | after removing duplicates |  cis proximal (<20kb) | cis long range | trans-contacts |
| :--------: | ----------: | ------- | - | -----: | - | ------------------------- |  --------------------- | - | -----------------|
| MARGI-1 | 72,969,293 | 64,200,403 | 88% | 20,544,129 | 38% | 2,319,120  |  71% | 1 % | 28% |
 




