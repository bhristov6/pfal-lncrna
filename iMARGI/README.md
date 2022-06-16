# iMARGI

The paper describing the iMARGI-seq protocol is here [paper](https://www.biorxiv.org/content/10.1101/681924v1.full.pdf). I ran manually the scripts instead of the Docker container provided by the paper's authors. 


I downloaded the data iMARGI data Trevor sent me (total of 5 pair-end experiemts) into [~proj/Data/LeRochLab/iMARGI](~proj/Data/LeRochLab/iMARGI). It appears the two experiments did not work out properly since the vast majority of the valid pairs are from proximal contacts (<10kb). Further, the distal cis/trans ratio is close to that of uniform distribution:

The theoretical expectation


distal cis = 8.45\%
trans = 91.55\%



| experiment | total reads | after filtering | mapped |  non duplicates |  cis proximal (<10kb) | cis distal (>10kb) | trans-contacts | final valid pairs |  %  |
| :--------: | ----------- | --------------- | ------ |  -------------- |  ---------------------| ------------------ | ---------------| ------------------| --- |
| Human     | 361,159,664  | 72%             | 65%    |  96%            |  44%  (<200kb)                 | 10 %              | 46.0%           |    24,316,461       |  10^-3% |
| :--------: | ----------- | --------------- | ------ |  -------------- |  ---------------------| ------------------ | ---------------| ------------------| --- |
| iMARGI-1   | 72,969,293  | 65%             | 85%    |  26%            |  97%                  | 0.27 %              | 3.0%           |    412,057       |  10^-3% |
| iMARGI-2   | 89,217,353  | 58%             | 82%    |  29%            |  97%                  | 0.27 %              | 2.9%           |    421,814       |  10^-3% |
| iMARGI-3   | 55,759,881  | 55%             | 58%    |  28%            |  96%                  | 0.30 %              | 3.7%           |    56,577       |  10^-3% |
| iMARGI-4   | 32,403,152  | 61%             | 81%    |  23%            |  96%                  | 0.40 %              | 3.8%           |    363,935       |  10^-3% |
| iMARGI-5   | 63,998,107  | 54%             | 92%    |  24%            |  96%                  | 0.33 %              | 3.6%           |    401,322       |  10^-3% |