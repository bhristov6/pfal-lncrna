# iMARGI

The paper describing the iMARGI-seq protocol is here [paper](https://www.biorxiv.org/content/10.1101/681924v1.full.pdf). I ran manually the scripts instead of the Docker container provided by the paper's authors. 


I downloaded the data iMARGI data Trevor sent me (total of 5 pair-end experiments) into [~proj/Data/LeRochLab/iMARGI](~proj/Data/LeRochLab/iMARGI). Working on getting the scripts to run bug free. 

## Basic statistics.

| experiment | total reads | cleaned | % |  mapped | % | after removing duplicates | % | after filter proximal (<20kb) | % | trans-contacts % |
| :--------: | ----------: | ------- | - | -----: | - | ------------------------- | - | --------------------- | - | -----------------|
| MARGI-4 | 32,403,152 | 27,801,922 | 85% | 12,510,865 | 45% | 1,414,669 | 11% | 505,543 | 35% | 84 % |
| MARGI-1 | 72,969,293 | 64,200,403 | 88% | 20,544,129 | 38% | 2,319,120 | 11% | 152,992 | 10% | 91 % |





