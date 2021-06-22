# plasmo-lncrna
Plasmodium lncRNA investigation with the Le Roch lab.

All of the downloaded data is in: /net/noble/vol1/home/borislav/proj/Data/LeRochLab/2021_ChIRP_RawFiles

All processed data and results are in: /net/noble/vol1/home/borislav/proj/2021_borislav_plasmo-chirp/Outputs




## Peak Genome Browser Visualization

Full figures size are in [Figures/peaks_genome_viz](Figures/peaks_genome_viz)

![TARE_dist](Results/peaks_igv/TARE.png)

![TARE_dist](Results/peaks_igv/lnc13.png)

![TARE_dist](Results/peaks_igv/lnc178.png)

![TARE_dist](Results/peaks_igv/lnc271.png)

![TARE_dist](Results/peaks_igv/lnc1494.png)

![TARE_dist](Results/peaks_igv/ch9.png)

![TARE_dist](Results/peaks_igv/ch14.png)


## Peaks Locations and Heights

Peaks' coordinates for each lncRNA are in .bed file format here: [Peak Locations](Results/top_peaks_location)

## Increase expression of genes near the peaks

Genes that are near the peaks have their expression statistically significantly increased in the respective lncRNA active stage.

![TARE_dist](Results/gene_expression.png)

## Overlap with 3' and 5' UTRs and genes

The peaks overlap predominately with the 5' flank and body of the genes.

![TARE_dist](Results/peak_overlap.png)


## Changes in Nucleosome and Histone activity 

All figures in full sizes are here: [Figures/Histone_and_Nucleosome](Figures/Histone_and_Nucleosomez)

For several histone marks we observed very strong change in activity, i.e:

![TARE_dist](Results/Hist_new/lnc13_H3K36me2.png)

![TARE_dist](Results/Hist_new/lnc13_H4K20me3.png)

![TARE_dist](Results/Hist_new/lnc13_H3K9ac.png)


---

***

Lab book notes and more technical intermediary figures below

---

***




## TARE

TARE peaks have been called via MACS2 and PePr using as a control the Schizont Input files as well as the tRNA files. Adding the tRNA tracks didnot change any of the top peaks and had a minor effect removing some of the small peaks (height < 150). All approaches yielded a set of 749 peaks in common, among them the top 18 peaks persistently present.   



|         | PePr           | MACS2  |  PePr (+tRNA) |MACS2 (+tRNA) | in common |
| ------------- |:-------------:| -----:| -----:| -----:| -----:|
| num peaks      | 1265 | 2151 | 1164| 1875|749|

<br/><br/>
Looking at where the peaks are given their raw (normalized height):

![TARE_dist](Results/h_macsTARE_4tRNA_peaks.png)

<br/><br/>

Interestingly, the summit of the top 18 peaks are all 20-30kb from a var gene while the other peaks sit either right next to (<1kb) or at myriad of other distances. I'm not sure if this is relevant though, it doesn't seem to me to be a coincidence. 

![TARE_dist](Results/dist_to_var.png)

<br/><br/>
The top peaks also exhibit a much stronger nucleosome signal compared to those with height less than 150.

![TARE_dist](Results/TARE_top250_nucleosome_znorm.jpeg)
![TARE_dist](Results/TARE_bottom100_nucleosome_znorm.jpeg)

<br/><br/>
Examining a larger window (20000 bases instead of 2000b) reaffirms the results:
![TARE_dist](Results/TARE_nucleosome_znorm10.jpeg)

<br/><br/>
Histone marks analysis is available here: [Histone Analysis](Results/NR/nucleosome.html).

<br/><br/>

## Differential biding of lncRNAs active in different stages.

### Methodology

I applied two conceptually different approaches. Starting with the mapped reads:

![TARE_dist](Results/step0.png)

<br/><br/>

#### A.1 MACS2 + DiffBind

First we call separately peaks in the active and non-active stage using the corresponding inputs to find where the lncRNA binds to.

![TARE_dist](Results/step1.png)

Then, we feed these two sets of peaks in DiffBind to obtain the set of differential peaks.

![TARE_dist](Results/step2.png)

#### A.2 PePr

Alternatively, PePr [paper_here](https://pubmed.ncbi.nlm.nih.gov/24894502/), designed with this goal in mind, uses all inputs simultaneously to build a model and call the set of differential peaks.

![TARE_dist](Results/stepP.png)

### Results

Encouragingly, the two approaches yielded very similar results:


|         lncRNA           | MACS2 + DiffBind  |  PePr | in common |
| ------------- |:-------------:| -----:| -----:|
| lnc13      | 844 | 558 | 551| 
| lnc178      | 362 | 157 | 154| 
| lnc271      | 1165 | 562 | 531| 
| lnc1494      | 1348 | 850 | 765| 
| lnc ch9      | 426 | 7 | 4 | 
| lnc ch14      | 1107 | 912 | 866 | 

[Nucleosome Analysis](Results/NR/nucleosome.html)
<br/><br/>
[Histone Analysis](Results/NR/nucleosome.html):
* [lnc13](Results/NR/lnc13.html)
* [lnc178](Results/NR/lnc178.html)
* [lnc271](Results/NR/lnc271.html)
* [lnc1494](Results/NR/lnc13.html)
* [lnc ch14](Results/NR/lnc13.html)


This analysis have changed a bit since I focused only on the tallest peaks. Some of the signal, especially for [lnc13](https://github.com/bhristov6/plasmo-lncrna/blob/main/Results/DB/13.html), become much stronger.

[Updated Histone and Nucleosome Analysis](https://github.com/bhristov6/plasmo-lncrna/blob/main/Results/DB2/nucleosome.html)


#### GO enrichment Analysis

Unfortunately, nothing of significance popped out when looking at the genes that are within 1000b from the top 10% of lncRNA peaks. Initially, I thought that because not all summits have a gene within the specified distance I have very few genes for a meaningful GO enrichment test. However, looking at all peaks and expanding the distance threshold to 2000b yielded the same result of no significant GO terms found.

![TARE_dist](Results/go.png)

#### Differential Expression Analysis

I looked at the genes that are within 1000b from the summit of the top 10% of lncRNA peaks and plotted their expression of active v non-active stage with the black line being the 45degree x=y. 

![TARE_dist](Results/DE/lnc13.png)

![TARE_dist](Results/DE/lnc178.png)

![TARE_dist](Results/DE/lnc271.png)

![TARE_dist](Results/DE/lnc1494.png)




A plot of the background (all genes):

![TARE_dist](Results/DE/all.png)

***

<br/><br/>

#### Differential Expression Analysis

Here are more informative violin plots of the log fold change of the expression of the nearest genes (but not further than 1000b from a peak) as I looked at the top 10% of the tallest peaks, the middle 10%, and the bottom 10%, as well as all genes so that we can see the background. Clearly, the top 10% differ from the background and the difference becomes more prominent as we consider only the top peaks.

![TARE_dist](Results/DE_new/lnc13.png)

![TARE_dist](Results/DE_new/lnc178.png)

![TARE_dist](Results/DE_new/lnc271.png)

![TARE_dist](Results/DE_new/lnc1494.png)



#### Nucleosome/Histone Analysis

I added the standard deviation as shade to the plots previously generated and also considered separately the top 10% versus the bottom 10% of the peaks. Not surprisingly, the tallest peaks exhibited strong signal while the bottom ones did not show any signal further supporting our hypothesis that the tallest peaks are the real biologically relevant peaks we should be focusing on. 


The first plot is ALL peaks.

![TARE_dist](Results/Nucl_new/lnc13_nucleosome_znorm_ALL.jpeg)



Top 10% of tallest peaks

![TARE_dist](Results/Nucl_new/lnc13_nucleosome_znorm_TOP.jpeg)

Bottom 10% of peaks

![TARE_dist](Results/Nucl_new/lnc13_nucleosome_znorm_bottom.jpeg)

***

Here, each row in the heat plot correspond to one peak, the peaks are sorted according to their height with the tallest peaks on the top, the center is at the summit of each peak, and as before a 1000b window around the summit of each peak was considered and the nucleosome values plotted in the corresponding color. Very clearly, the signal is located at the top middle section of the heat plot.

![TARE_dist](Results/Nucl_new/lnc13_ALL.png)

***

The histone mods plots are similar with exhibiting the same trend: signal located at the middle top. A selected few plots are displayed below.

![TARE_dist](Results/Hist_new/lnc13_H3K9ac_znorm.jpeg)

![TARE_dist](Results/Hist_new/lnc13_H3K9ac.png)

***

![TARE_dist](Results/Hist_new/lnc13_H3K36me2_znorm.jpeg)

![TARE_dist](Results/Hist_new/lnc13_H3K36me2.png)

***

![TARE_dist](Results/Hist_new/lnc13_H4K20me3_znorm.jpeg)

![TARE_dist](Results/Hist_new/lnc13_H4K20me3.png)


---

#### Peak genome wide locations

I examined what regions in the genome the peaks overlap. A couple of caveats, I have 5'/3' UTR annotations for 4875 genes; not all genes have multiple exons so first/last/internal exon/intron are not always meaningful.

![TARE_dist](Results/seg/13_all.png)

![TARE_dist](Results/seg/178_all.png)

![TARE_dist](Results/seg/271_all.png)

![TARE_dist](Results/seg/1494_all.png)


#### Peak Genome browser Visualization

![TARE_dist](Results/peaks_igv/TARE.png)

![TARE_dist](Results/peaks_igv/lnc13.png)


