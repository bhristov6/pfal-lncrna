15-Aug-2021

1) Created a 2-order background from the two sets of sequences.
  cat seq_500_long/lnc*.txt > ! seq_500_long/lnc.all.fa
  fasta-get-markov -m 2 < seq_500_long/lnc.all.fa > seq_500_long/lnc_all.m2.bg

2) Ran SEA using this common background model on each sequence file
separately, and contrasting top25 with bot_75:
  mkdir results/seq_500_long
  sea -p seq_500_long/lnc13_top25.txt -m motif.html -inc '1-*' -bfile seq_500_long/lnc_all.m2.bg -oc results/seq_500_long/sea_top25
  sea -p seq_500_long/lnc13_bot75.txt -m motif.html -inc '1-*' -bfile seq_500_long/lnc_all.m2.bg -oc results/seq_500_long/sea_bot75
  sea -p seq_500_long/lnc13_top25.txt -n seq_500_long/lnc13_bot75.txt -m motif.html -inc '1-*' -bfile seq_500_long/lnc_all.m2.bg -oc results/seq_500_long/sea_top25_vs_bot75
  sea -p seq_500_long/lnc13_top25.txt -n seq_500_long/random_seq.txt -m motif.html -inc '1-*' -bfile seq_500_long/lnc_all.m2.bg -oc results/seq_500_long/sea_top25_vs_random

4) Ran MAST on each of the datasets.
  mast -oc results/seq_500_long/mast_top25 -mi 1 motif.html seq_500_long/lnc13_top25.txt
  mast -oc results/seq_500_long/mast_bot75 -mi 1 motif.html seq_500_long/lnc13_bot75.txt
  mast -oc results/seq_500_long/mast_random -mi 1 motif.html seq_500_long/random_seq.txt

14-Aug-2021
1) Created a 2-order background from the two sets of sequences.
  cat lnc*.txt > ! lnc.all.fa
  fasta-get-markov -m 2 < lnc_all.fa > lnc_all.m2.bg

2) Ran SEA using this common background model on each sequence file
separately, and contrasting top25 with bot_75:
  sea -p lnc13_top25.txt -m motif.html -inc '1-*' -bfile lnc_all.m2.bg -oc results/sea_top25
  sea -p lnc13_bot75.txt -m motif.html -inc '1-*' -bfile lnc_all.m2.bg -oc results/sea_bot75
  sea -p lnc13_top25.txt -n lnc13_bot75.txt -m motif.html -inc '1-*' -bfile lnc_all.m2.bg -oc results/sea_top25_vs_bot75
  sea -p lnc13_top25.txt -n random_seq.txt -m motif.html -inc '1-*' -bfile lnc_all.m2.bg -oc results/sea_top25_vs_random

3) The AT content of the random genomic sequences is much higher than the
top 25% seqences (about 80% AT vs 72%):
> fasta-get-markov lnc13_top25.txt
  # 0-order Markov frequencies from file lnc13_top25.txt
  # seqs: 138    min: 100    max: 100    avg: 100.0    sum: 13800    alph: DNA
  # order 0
  A 3.568e-01
  C 1.432e-01
  G 1.432e-01
  T 3.568e-01
  > fasta-get-markov lnc13_bot75.txt
  # 0-order Markov frequencies from file lnc13_bot75.txt
  # seqs: 413    min: 100    max: 100    avg: 100.0    sum: 41300    alph: DNA
  # order 0
  A 3.878e-01
  C 1.122e-01
  G 1.122e-01
  T 3.878e-01
  > fasta-get-markov random_seq.txt
  # 0-order Markov frequencies from file random_seq.txt
  # seqs: 10000    min: 84    max: 100    avg: 100.0    sum: 999984    alph: DNA
  # order 0
  A 4.029e-01
  C 9.710e-02
  G 9.710e-02
  T 4.029e-01

4) Ran MAST on the top25% sequences.

