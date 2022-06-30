# RADICL-seq

The paper describing the RADICL-seq protocol is here [paper](https://www.biorxiv.org/content/10.1101/681924v1.full.pdf). Basically, the setup is:


**RNA sequence (27 nt) --- Forward bridge (50nt) --- DNA sequence (27 nt)**

**DNA sequence (27 nt) --- Reverse bridge (50nt) --- RNA sequence (27 nt)**

where

**Forward bridge**: CTGCTGCTCCTTCCCTTTCCCCTTTTGGTCCGACGGTCCAAGTCAGCAGT

**Reverse bridge**: ACTGCTGACTTGGACCGTCGGACCAAAAGGGGAAAGGGAAGGAGCAGCA


I downloaded the data new RADICL-seq data Trevor/Seven sent me (\_2021\_11, \_2022\_01 and \_2022\_03) into [~proj/Data/LeRochLab/RADICL](~proj/Data/LeRochLab/RADICL) and processed it the same way as the original one. It appears the two experiments did not work out as only a tiny fraction of the reads contain the bridge (<1%). 

The latest experiment from Trevor seems to have worked out much better than the previous ones- the bridge is now found in 8% of the reads (compared to 1% previously) though still far below the 42% of the original run. Here are some statistics that might be helpful. 

## Basic statistics and comparison to the earlier experiment.

| experiment | total reads | length | having bridge | % |
| :--------: | -----------: | ------ | -------------: | - |
| Original\_2021\_03<sup>1</sup>| 23,151,097 | 151 (0.54) | 9,750,719 | 42.1% |
| New\_2021\_11<sup>2</sup> | 348,340,949 | 101 (0) | 768,611 | 0.2% |
| New\_2022\_01<sup>3</sup> | 81,825,527 | 151 (0.79) | 982,801 | 1.0% |
| New\_2022\_03<sup>4</sup> | 124,464,083 | 151 (0) | 10,161,011 | 8.1% |
| New\_2022\_03<sup>5</sup> | 169,116,426 | 151 (0) | 685,964 | 0.4% |


After extracting the RNA and DNA tags and aligning them to the plasmodium genome I'm left with the following:


| type | total tags | length | align uniquely | % | align multiple | % | align to human | % |
| ---- | :--------: | -------| ---------------| - | -------------- | - | -------------- | - | 
| DNA<sup>1</sup> | 9,733,215 | 27 | 2,688,848 | 27.6% | 768,242      | 7.9% | 5,752,330 | 58.1% |
| RNA<sup>1</sup> | 9,734,742 | 27 | 812,473 | 8.3% | 2,381,550      | 24.4% | 5,977,131 | 61.4% |
| DNA<sup>2</sup> | 747,725 | 19.2 | 226,932 | 30.3% | 171,095     | 22.9% | 334,979 | 44.8% |
| RNA<sup>2</sup> | 746,392 | 17.5 | 30,602 | 4.1% | 138,082     | 18.5% | 298,556 | 40.1% |
| DNA<sup>3</sup> | 931,442 | 19.4 | 270,118 | 29.1% | 232,860     | 24.8% | 393,989 | 42.3% |
| RNA<sup>3</sup> | 930,956 | 17.9 | 46,570 | 5.0% | 138,082     | 18.5% | 381,691 | 41.2% |
| DNA<sup>4</sup> | 10,154,669 | 26.1 | 4,796,946 | 47.2% | 1,199,216     | 11.8% | 1,500,823 | 14.7% |
| RNA<sup>4</sup> | 9,971,112 | 24.7 | 2,333,526 | 23.4% | 1,773,374     | 17.4% | 961,768 | 9.6% |


Experiments <sup>2</sup> and <sup>3</sup> did not work out well as very few of trheir reads contain the bridge (<1%). Karine explained that it is difficult to get the protocol to work correctly; it is also very poorly described in the methods section of the published paper. 
Similar to the very first time the RADICL experiment was done, the DNA tags align uniquely much better than the RNA tags which align multiple times. Also in all experiments significant chunk of the DNA and RNA tags align to the human genome. These observations are understandable/expected. 


I also checked if the sequences that do not contain the bridge align to the human genome but that was not the case.

| experiment | sequences | align to human |
| --------- | --------- | -------------- |
| New\_2021\_11<sup>2</sup> | NO_bridge | 2.7% |
| New\_2022\_01<sup>3</sup> | NO_bridge | 3.5% |


Finally, the number of pairs of RNA-DNA tags for which both tags align uniquely to the plasmodium genome and hence we can use to investigate interactions are very very few:

| experiment | start with | left with |
| --------- | -------------- | - |
| New\_2021\_11<sup>2</sup> | 348,340,949 | 24,275 |
| New\_2022\_01<sup>3</sup> | 81,825,527 | 44,352 |
| New\_2022\_03<sup>4</sup> | 124,464,083 | 412,057 |




## Latest RADICL


| experiment | total reads | having the bridge | mapped |  non duplicates |  cis proximal (<10kb) | cis distal (>10kb) | trans-contacts | final valid pairs | 
| :--------: | ----------- | --------------- | ------ |  -------------- |  ---------------------| ------------------ | ---------------| ------------------|
| RADICL4 (March)   | 124,464,083  | 8.1%             | 47%    |  8.8%            |  2%                  | 7 %              | 91%           |    412,057       |  
| RAD7H     | 9  |              |     |             |                   |              |            |           |   |
| RAD9   | 126,296,385  | 9%             | 56%    |  9.8%            |  1%                  | 9 %              | 90%           |    443,636       |  
| RAD10     | 16 |              |     |             |                   |              |            |           |   |
| Undetermined   | 18,466,857  | 0.5%             | 51%    |  8.5%            |  1%                  | 8 %              | 90%           |    28       |  
| iMARGI1     | 72,969,293 |      222        |     |             |                   |              |            |           |   |
| iMARGI2     | 89,217,353 |       1054       |     |             |                   |              |            |           |   |
| iMARGI3     | 55,759,881 |     720         |     |             |                   |              |            |           |   |
| iMARGI4     | 32,403,152 |   466           |     |             |                   |              |            |           |   |
| iMARGI5     | 63,998,107 |   916           |     |             |                   |              |            |           |   |
