import numpy as np
import os
import sys
import math
import random
import time
import gzip



# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #



H = "/net/noble/vol1/home/borislav/"
P = f"{os.path.dirname(os.path.abspath(__file__))}/../"
T = f"{P}Temp/"
O = f"{P}Outputs/"
D = f"{P}Data/"
LD = f"{P}../0LargeData/Radicl/"
DD = "/Users/bhristov6/Desktop/"

BPATH = os.path.dirname(os.path.abspath(__file__))

if BPATH[0:10] == "/net/noble":
	LD = "/net/noble/vol1/home/borislav/proj/Data/LeRochLab/"








# --------------------------------------------------------------------------- #
# Basic timer
# --------------------------------------------------------------------------- #

def print_time_taken(start_time, task_name=""):
	t = time.time() - start_time
	st = "done " + task_name + " after = "
	if t < 60:
		st += (str(round(t,1)) + " sec")
	elif t < 3600:
		st += (str(round(t/60,1)) + " min")
	else:
		st += (str(round(t/3600,2)) + " h")
	print(st)
	


# --------------------------------------------------------------------------- #
# Create or Read bin maps
# --------------------------------------------------------------------------- #
	
# read bin map
def read_bin_map():
	chr_map, bin_map = {}, {}
	
	for line in open(f"{P}Data/bin_maps/bin_map_{bin_size}.bed"):
		words = line.rstrip().split("\t")
		chr   = int(words[0])
		start = int(words[1])
		end   = int(words[2])
		bin   = int(words[3])
		
		if chr not in chr_map:
			chr_map[chr] = []
			
		chr_map[chr].append([start, end, bin])
		bin_map[bin] = (chr, start, end)
	
	nbins = max(bin_map.keys()) + 1
	print("nbins = " + str(nbins))
	return (chr_map, bin_map, nbins)




# returns the bin corresponding to the given genomic coordinates
def get_bin_from_chr_loc(chr, loc):
	x = int(loc/bin_size)
	
	# Fit-Hi-C mess: return the last bin if mid fragment is outside of it
	if x >= len(chr_map[chr]):
		t = chr_map[chr][-1]
		if loc >= t[1] and loc < (t[1] + bin_size):
			return t[2]
		else:
			raise ValueError("location " + str(loc) + " is outside of chromosome " + str(chr))
	else:
		return chr_map[chr][x][2]








# --------------------------------------------------------------------------- #
# read known lncRNAs
# --------------------------------------------------------------------------- #

# read the excel sheet of known lncRNAs to get their coordinates
def read_lncRNAs(subset=True):
	fname = (f"{D}lnc_chirp.tsv" if subset else f"{D}lnc_all.tsv")
	
	lncRNAs = {}
	
	for line in open(fname):
		words = line.rstrip().split("\t")
		lncRNAs[words[0]] = {}
		lncRNAs[words[0]]["chr-Pf"] = words[1]
		lncRNAs[words[0]]["chr"] = int(words[1].split("_")[1])
		lncRNAs[words[0]]["start"] = int(words[2])
		lncRNAs[words[0]]["end"] = int(words[3])

	return lncRNAs







# --------------------------------------------------------------------------- #
# read gff file
# --------------------------------------------------------------------------- #

def read_GFF_file():
	global gff_dict_genes, gff_dict_bins
	gff_dict_genes, gff_dict_bins = {}, {}
	gene_types, feature_types = [], []
	start_time, num_lines = time.time(), 0
	
	for line in open('/Users/bhristov6/Desktop/Code/base/Data/Plasmo/PlasmoDB-9.0_Pfalciparum3D7.gff'):
		words = line.rstrip().split("\t")
		
		# the genome sequence is below- we don't need it right now
		if words[0] == "##FASTA":
			print("encountered ##FASTA")
			break
			
		if words[0][0] == "#": continue 
		
		# feature_types.append(words[2]) # explore: what features are in this gff?
		
		if words[2] != "gene": continue
		
		gene      = words[8].split(";")[0][3:].split(".")[0]
		gene_type = words[8].split(";")[2][10:] # gene_types.append(gene_type) # explore: what types of genes are in this gff?
		tss       = int(words[3] if words[6] == "+" else words[4])
		
		
		# if chrM or PF_M7661: skip
		if "API" in words[0] or "M" in words[0]:
			continue

		chr = int(words[0].split("_")[1])
		
		if words[2] != "gene":
			continue
		
		# finally, get the bin and populated the hashes
		bin  = get_bin_from_chr_loc(chr,tss)
		
		gff_dict_genes[gene] = (chr, tss, bin)
		
		if not bin in gff_dict_bins: gff_dict_bins[bin] = []
		gff_dict_bins[bin].append(gene)


	print_time_taken(start_time, "reading gff file with " + str(len(gff_dict_genes)) + " genes")
	return (gff_dict_genes, gff_dict_bins)



# --------------------------------------------------------------------------- #
# write down basic array and matrix
# --------------------------------------------------------------------------- #


# write down the matrix in basic format: bin_i bin_j val
def write_matrix(a, fname, write_vals_above = 0, upper_half = False):
	fo = open(fname, "w")
	
	for i in range(a.shape[0]):
		for j in range(a.shape[1]):
			if upper_half and j > i:
				continue
			if a[i][j] > write_vals_above:
				fo.write(str(i) + "\t" + str(j) + "\t" + str(a[i][j]) + "\n")
	fo.close





# --------------------------------------------------------------------------- #
# Generate mcool file from our npy matrix
# --------------------------------------------------------------------------- #


def generate_mcool(a, fname):
	
	# See: https://cooler.readthedocs.io/en/latest/cli.html#cooler-load
	
	
	# 1. write the matrix into COO format
	write_matrix(a, f"{T}{fname}.txt", 0, upper_half = False)
	print(f"da\n")
	# 2. call cooler
	os.system(f"cooler load -f coo {P}Data/chrom_lengths.txt:10000 {T}{fname}.txt {T}{fname}.cool --no-symmetric-upper")
	os.system(f"cooler zoomify {T}{fname}.cool")
	os.remove(f"{T}{fname}.txt")
	os.remove(f"{T}{fname}.cool")





def write_array(array, fname):
	fo = open(fname, "w")
	for i in range(len(array)):
		fo.write(f"{i}\t{array[i]}\n")










# --------------------------------------------------------------------------- #
# Read at once all fixed inputs such as chr ids, lengths, etc
# --------------------------------------------------------------------------- #

# reads all of the fixed data
def read_fixed_data(res):
	global bin_size, chr_map, bin_map, nbins
	bin_size = res
	
	(chr_map, bin_map, nbins) = read_bin_map()
	return (chr_map, bin_map, nbins)










# --------------------------------------------------------------------------- #
# NO Executable
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
	pass
