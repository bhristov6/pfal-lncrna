# iMARGI

The paper describing the iMARGI-seq protocol is here [paper](https://www.biorxiv.org/content/10.1101/681924v1.full.pdf). I ran manually the scripts instead of the Docker container provided by the paper's authors. 


I downloaded the data iMARGI data Trevor sent me (total of 5 pair-end experiemts) into [~proj/Data/LeRochLab/iMARGI](~proj/Data/LeRochLab/iMARGI). It appears the two experiments did not work out properly since the vast majority (97%)of the valid pairs are from proximal contacts (<10kb) reprsenting nascent transcripts. Further, the distal cis/trans ratio is close to that of uniform distribution which theoretical expectation is:

distal cis = 8.45\%
trans = 91.55\%

38,434,899

| experiment | total reads | after filtering | mapped |  non duplicates |  cis proximal (<10kb) | cis distal (>10kb) | trans-contacts | final valid pairs |  %  |
| :--------: | ----------- | --------------- | ------ |  -------------- |  ---------------------| ------------------ | ---------------| ------------------| --- |
| Human     | 361,159,664  | 72%             | 65%    |  96%            |  43%  (<200kb)                 | 10 %              | 47.%           |    38,434,899       |  10.6% |
| iMARGI-1   | 72,969,293  | 65%             | 85%    |  26%            |  97%                  | 0.27 %              | 3.0%           |    412,057       |  0.5% |
| iMARGI-2   | 89,217,353  | 58%             | 82%    |  29%            |  97%                  | 0.27 %              | 2.9%           |    421,814       |  0.4% |
| iMARGI-3   | 55,759,881  | 55%             | 58%    |  28%            |  96%                  | 0.30 %              | 3.7%           |    56,577       |  0.1% |
| iMARGI-4   | 32,403,152  | 61%             | 81%    |  23%            |  96%                  | 0.40 %              | 3.8%           |    363,935       |  1.0% |
| iMARGI-5   | 63,998,107  | 54%             | 92%    |  24%            |  96%                  | 0.33 %              | 3.6%           |    401,322       |  0.6% |
| |
| *New August Data* |
| Undetermined | 67,050,785 | 41% | 23% |  21% | 99% | 0.05% | 0.9% | 81,622 | 0.1% |
| Ring | 7,319,365 | 39% | 38% | 20% | 99% | 0.03% | 1% | 8,315 | 0.1% |
| Schizont | 18,623,459 | 44% | 25% | 20% | 99% | 0.08% | 0.9% | 24,581 | 0.1% | 
