#!/bin/bash


# 3. Run samtools to clean up the reads

# 3.0 sort the .sam to .bam
samtools sort -o $1.bam $1.sam

# 3.1 sort by name 
samtools sort -n -o $1\_n.bam $1.bam
# 3.2 add ms and MC tags for markdup to use later
samtools fixmate -m $1\_n.bam $1\_nf.bam
# 3.3 sort by position
samtools sort -o $1\_nfs.bam $1\_nf.bam
# 3.4 mark duplicates
samtools markdup -s $1\_nfs.bam $1\_d.bam

# 3.5 remove dulicates, unmapped, and low quality reads
samtools view -F 1796 -b -o $1\_f1.bam $1\_d.bam

# 3.6 now apply the -q 20 filtering removing reads with MAPQ < 20
samtools view -q 20 -b $1\_f1.bam > $1\_filtered.bam


# 3.7 index the file
samtools index $1\_filtered.bam

# 3.8 obtain basic statistics
samtools idxstats $1\_filtered.bam >> $1\_filtered_stats.txt
samtools flagstat $1\_filtered.bam >> $1\_filtered_stats.txt

# 3.9 also compute depth
samtools depth -a $1\_filtered.bam >> $1\_filtered_depth.txt

# 3.10 call bedtools to get a bed file
bedtools bamtobed -i $1\_filtered.bam > $1\_filtered.bed

# 4. clean up removing intermediary files
#rm $1.sam
rm $1.bam
rm $1\_n.bam
rm $1\_nf.bam
rm $1\_nfs.bam
rm $1\_d.bam
rm $1\_f1.bam


