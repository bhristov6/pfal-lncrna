import numpy as np
import os
import sys
import random
import time
import gzip



# --------------------------------------------------------------------------- #
# Timers
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
# Read Core Input Files
# --------------------------------------------------------------------------- #

# read bin map
def read_bin_map(fname):
	chr_map, bin_map = {}, {}
	
	for line in open(fname):
		words = line.rstrip().split("\t")
		chr   = get_chr_id_bobby_MESS2(words[0])
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


def get_chr_id_bobby_MESS(chr_name_in):
	if is_human: return chr_names_to_ids[f"{chr_name_in}"]
	return int(chr_name_in)


def get_chr_id_bobby_MESS2(chr_name_in):
	if is_human: return chr_names_to_ids[f"chr{chr_name_in}"]
	return int(chr_name_in)-1

# --------------------------------------------------------------------------- #
# Chromosome names and IDs
# --------------------------------------------------------------------------- #



def define_plasmo_chr_ids():
	chr_ids = list(range(14)) # THIS EXCLUDES API and M76611. Set to 16 if you want to include
	chr_ids_to_names, chr_names_to_ids = {}, {}
	
	for i in range(0,9):
		chr_ids_to_names[i] = f"Pf3D7_0{i+1}_v3"
		chr_names_to_ids[f"Pf3D7_0{i+1}_v3"] = i
	for i in range(9,14):
		chr_ids_to_names[i] = f"Pf3D7_{i+1}_v3"
		chr_names_to_ids[f"Pf3D7_{i+1}_v3"] = i
	
	# THIS EXCLUDES API and M76611. Set to TRUE if you want to include
	if False:
		chr_names_to_ids["Pf3D7_API_v3"] = 14
		chr_names_to_ids["Pf_M76611"]    = 15
		chr_ids_to_names[14] = "Pf3D7_API_v3"
		chr_ids_to_names[15] = "Pf_M76611"
	
	return (chr_ids, chr_ids_to_names, chr_names_to_ids)


def define_human_chr_ids():
	chr_ids = list(range(24))
	chr_ids_to_names, chr_names_to_ids = {}, {}
	
	for i in range(22):
		chr_ids_to_names[i] = f"chr{i+1}"
		chr_names_to_ids[f"chr{i+1}"] = i

	chr_names_to_ids["chrX"] = 22
	chr_names_to_ids["chrY"] = 23
	chr_ids_to_names[22] = "chrX"
	chr_ids_to_names[23] = "chrY"
	
	return (chr_ids, chr_ids_to_names, chr_names_to_ids)

def read_chr_length(fname):
	chr_length = {}
	for line in open(fname):
		words = line.rstrip().split("\t")
		chr_length[chr_names_to_ids[words[0]]] = int(words[1])
		
	return chr_length



# --------------------------------------------------------------------------- #
# obsolete


# we are going to only use 1-23 and skip special regions
def define_human_chromosome_names():
	chromosome_names = [str(i) for i in range(1,23)]
	chromosome_names.append("X")
	chromosome_names.append("Y")
	return chromosome_names

# we are going to use only the chromosomes and skip the two plastids
def define_plasmo_chromosome_names():
	chromosome_names = [str(i) for i in range(1,15)]
	#chromosome_names.append("API")
	#chromosome_names.append("M76611")
	return chromosome_names


# --------------------------------------------------------------------------- #


# at what bins do the centromeres fall
def read_centromeres(fname, window_size):
	centromere_bins = set()

	with open(fname, "r") as f:
		next(f)
		for line in f:
			words = line.rstrip().split("\t")
			bin1 = get_bin_from_chr_loc(chr_names_to_ids[words[0]], int(words[1]))
			bin2 = get_bin_from_chr_loc(chr_names_to_ids[words[0]], int(words[2]))
			
			[centromere_bins.add(i) for i in range(bin1 - window_size, (bin2 + 1) + window_size)]
	
	return centromere_bins
	

# Read Plasmo virulence genes
def read_virulence_genes(fname):
	virulence_bins = {}
	
	with open(fname, "r") as f:
		next(f)
		for line in f:
			words = line.rstrip().split("\t")
			b = get_bin_from_chr_loc(chr_names_to_ids[words[1]], int(words[2]))
			if b in virulence_bins:
				virulence_bins[b].append(words[0])
			else:
				virulence_bins[b] = [words[0]]

	return virulence_bins


def read_RBM20_bins(fname):
	#return (0,0)
	rbm20_genes, rbm20_bins = {}, set()
	
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		for i in (0,1):
			gene  = words[i]
			loc   = words[i+7].replace("\"", "")
			#chr   = get_chr_id_bobby_MESS(loc.split(":")[0].replace("chr", ""))
			chr   = get_chr_id_bobby_MESS(loc.split(":")[0])
			start = int(loc.split(":")[1].split("-")[0].replace(",", ""))
			end   = int(loc.split(":")[1].split("-")[1].replace(",", ""))
			
			# fix errors in the table! There is an extra digit in a few places!!!!
			if (end - start) > 1000000:
				end = int(end/10)
		
			rbm20_genes[gene] = (chr, start, end)
		
			bin1 = get_bin_from_chr_loc(chr, start)
			bin2 = get_bin_from_chr_loc(chr, end)
			
			[rbm20_bins.add(i) for i in range(bin1, (bin2 + 1))]
		
	return (rbm20_genes, rbm20_bins)



# read the new excel file sent by Alessandro, parsed and wrote a simple list of bins file
def parse_new_RBM20():
	fo = open(TPATH + "RBM20_targets_new2.txt", "w")
	[fo.write(f"{bin}\n") for bin in set([gff_dict_genes[g][2] for g in [line.rstrip().split("\t")[0].split(":")[1] for line in open(f"{BASE}Data/Human/RBM20_targets_new2.txt")] if g in gff_dict_genes])]

def read_new_RBM20(fname):
	return [int(s) for s in [line.rstrip() for line in open(fname)]]



# read the compartments annotation file and for each bin assign it's score
def read_ABComp_single_file(fname):
	return 0
	compartments_map, num_line = {}, 0
	
	for line in open(fname):
		num_line += 1
		if num_line == 1: continue
		
		words = line.rstrip().split("\t")
		chr   = words[0]
		start = int(words[1])
		end   = int(words[2])
		
		for i in range(start, end, bin_size):
			bin = get_bin_from_chr_loc(chr, i)
			compartments_map[bin] = float(words[3])

	# some values are missing. Assume they are zero!
	for bin in bin_map:
		if bin not in compartments_map:
			compartments_map[bin] = 0
	
	print("read compartments map: " + fname)
	return compartments_map



def read_ABComp(fname):
	c1 = read_ABComp_single_file(f"Data/ABComp/{fname}_REP1_Active.PC1.bedGraph")
	c2 = read_ABComp_single_file(f"Data/ABComp/{fname}_REP2_Active.PC1.bedGraph")
	
	return [(c1[bin] + c2[bin])/2 for bin in bin_map]



# --------------------------------------------------------------------------- #
# read gff file
# --------------------------------------------------------------------------- #

def read_GFF_file(fname):
	gff_dict_genes, gff_dict_bins = {}, {}
	gene_types, feature_types = [], []
	start_time, num_lines = time.time(), 0
	
	for line in gzip.open(fname, "rt"):
		num_lines += 1
		words = line.rstrip().split("\t")
		
		# the genome sequence is below- we don't need it right now
		if words[0] == "##FASTA":
			print("encountered ##FASTA")
			break
			
		if words[0][0] == "#": continue 
		
		# feature_types.append(words[2]) # explore: what features are in this gff?
		
		if words[2] != "gene": continue
		
		gene      = words[8].split(";")[0][3:].split(".")[0]
		gene_type = words[8].split(";")[2][10:]
		tss       = int(words[3] if words[6] == "+" else words[4])
		chr       = str(words[0].replace("chr", ""))

		# gene_types.append(gene_type) # explore: what types of genes are in this gff?
		
		if chr not in chromosome_names: continue
		
		if gene_type != "protein_coding": continue
		
		# finally, get the bin and populated the hashes
		bin  = get_bin_from_chr_loc(chr,tss)
		
		gff_dict_genes[gene] = (chr, tss, bin)
		
		if not bin in gff_dict_bins: gff_dict_bins[bin] = []
		gff_dict_bins[bin].append(gene)


	print_time_taken(start_time, "reading gff file with " + str(len(gff_dict_genes)) + " genes")
	return (gff_dict_genes, gff_dict_bins)
	
	#[print(str(x) + ": " + str(gene_types.count(x))) for x in np.unique(gene_types)]
	#print("\n")
	#[print(str(x) + ": " + str(feature_types.count(x))) for x in np.unique(feature_types)]
	#print("\n")




# --------------------------------------------------------------------------- #
# Core Common Functions
# --------------------------------------------------------------------------- #

# return the bin correesponding to the given genomic coordinates
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



# find which rows are only zeros
def find_zero_and_non_zero_rows(a):
	zero_bins, non_zero_bins = [], []
	
	zr = np.all((a == 0), axis = 1)
	for i in range(len(zr)):
		if zr[i]:
			zero_bins.append(i)
		else:
			non_zero_bins.append(i)

	print("found number of rows with only zeros = " + str(len(zero_bins)))
	return (zero_bins, non_zero_bins)


# zero a band of the given size along the diagonal
def zero_diagonal_band(a, band_size):
	for i in range(len(a)):
		for j in range(max(0, (i - band_size)), min(len(a), (i + band_size + 1))):
			a[i][j] = 0
			a[j][i] = 0
	
	return a



# zero all cis-contacts and keep only trans contacts
def create_trans_contact_only_matrix(a):
	at = np.zeros((len(a),len(a)))
	
	for i in range(0, len(a)):
		for j in range(0, len(a)):
			if bin_map[i][0] == bin_map[j][0]:
				continue	
			at[i][j] = a[i][j]
	
	return at
	

def zero_centromere_bins(a):
	for b1 in centromere_bins:
		for b2 in centromere_bins:
			a[b1][b2] = 0
			a[b2][b1] = 0




# --------------------------------------------------------------------------- #
# Various handy functions
# --------------------------------------------------------------------------- #

def sort_hash_by_len(h):
	# h.items() return a list of tuples [(key1, h[key1]), (key2, h[key2]), ...] 
	# so we can sort it by whatever we need from x[1] 
	sort_orders = sorted(h.items(), key=lambda x: len(x[1]), reverse=True)
	sorted_keys = [x[0] for x in sort_orders]
	return sorted_keys
	
	# count condition in array
	# print(sum(g in ensmbl_dict for g in gff_dict_genes))
	
# print unique elements with number of occurences
def print_unique_el_with_num_occurences(arr):
	[print(str(x) + ": " + str(arr.count(x))) for x in np.unique(arr)]


def tar_directory(path_to_target, target):
	# tar requires to be executed from the location of the directory
	curr_dir = os.getcwd()
	os.chdir(path_to_target)
	os.system("tar -cf " + target + ".tar " + target + "/")
	os.chdir(curr_dir)


#a1 = np.load("Data/scrna_pcs10.npy")[np.ix_(idcs,idcs)]

# a = np.array(random.sample(list(range(1000)),20)).reshape((4, 5))

# --------------------------------------------------------------------------- #
# Outside tools matrix functions
# --------------------------------------------------------------------------- #


def ice_normalize_matrix(a, fname, bias_name):
	from iced import normalization
	from iced import filter

	counts = filter.filter_low_counts(a, percentage=0.05)
	(normed, bias) = normalization.ICE_normalization(counts, output_bias=True)
	
	# write the biases down
	fo = open(bias_name, "w")
	for i in bias:
		fo.write(str(i[0]) + "\n")
	
	# write the ICED matrix down
	write_matrix(normed, fname, False)


# not tested
def generate_mcool(fname):
	# See: https://cooler.readthedocs.io/en/latest/cli.html#cooler-load
	#
	
	os.system(str("cooler load -f coo Data/Processed/chrom_lengths.txt:10000 Temp/" + fname + "_c.txt Temp/" + fname + ".cool --field count:dtype=float"))
	os.system(str("cooler zoomify Temp/" + fname + ".cool"))
	os.remove(TPATH + fname + ".cool")
	os.remove(TPATH + fname + "_c.txt")




# --------------------------------------------------------------------------- #
# FitHic read files
# --------------------------------------------------------------------------- #

def read_fithic_output_gz(fname):
	start_time = time.time()
	num_zeros, num_nan, nrow = 0, 0, 0
	matrix = np.zeros((nbins,nbins))

	with gzip.open(fname, 'rt') as f:
		next(f)
		for line in f:
			nrow += 1
			words = line.rstrip().split("\t")

			i = get_bin_from_chr_loc(get_chr_id_bobby_MESS2(words[0]),int(words[1]))
			j = get_bin_from_chr_loc(get_chr_id_bobby_MESS2(words[2]),int(words[3]))
					
			if words[5] == "nan":
				num_nan += 1
				continue
			
			if float(words[5]) == 0:
				num_zeros += 1
				continue
			
			w = -np.log(float(words[5]))
			
			if w == 0:
				num_zeros += 1
				continue
				
			matrix[i][j] = w
			matrix[j][i] = w

	print("read data with nrow = " + str(nrow) + " num_nan = " + str(num_nan) + " num_zeros = " + str(num_zeros))
	print_time_taken(start_time, "reading Fit-Hi-C output")
	
	return matrix


# write down the matrix as interaction file of fragmentMid points (Fit-Hi-C format)
def write_interactions_fragments_file(a, fname):
	fo = open(fname, "w")
	
	for i in range(len(a)):
		for j in range(i, len(a)):
			if a[i][j] > 0:
				chr1 = bin_map[i][0]
				fr1  = bin_map[i][1] + bin_size/2
				chr2 = bin_map[j][0]
				fr2  = bin_map[j][1] + bin_size/2
				
				fo.write(chr1 + "\t" + str(int(fr1)) + "\t" + chr2 + "\t" + str(int(fr2)) + "\t" + str(int(a[i][j])) + "\n")
	fo.close()
	os.system("gzip " + fname)


# --------------------------------------------------------------------------- #
# Read and Write matrix
# --------------------------------------------------------------------------- #

# basic read matrix from our format
def read_matrix(fname, symmetric):
	start_time = time.time()
	matrix = np.zeros((nbins,nbins))
	
	for line in open(fname):
		words = line.rstrip().split("\t")
		i = int(words[0])
		j = int(words[1])
		w = float(words[2])
		 
		matrix[i][j] = w
		
		if symmetric:
			matrix[j][i] = w
	
	print_time_taken(start_time, "reading input matrix")
	if symmetric:
		print("  Treated the matrix as SYMMETRIC!!")
	return matrix



# write down the matrix in basic format: bin_i bin_j val
def write_matrix(a, fname, upper_half):
	fo = open(fname, "w")
	
	for i in range(len(a)):
		for j in range(len(a)):
			if upper_half and j > i:
				continue
			if a[i][j] > 0:
				fo.write(str(i) + "\t" + str(j) + "\t" + str(a[i][j]) + "\n")
	fo.close
	

# --------------------------------------------------------------------------- #
# read hashes
# --------------------------------------------------------------------------- #

def read_hashes():
	global hsh_entrz_ensmbl, hsh_ensmbl_entrz, hsh_entrz_human, hsh_human_entrz
	hsh_entrz_ensmbl, hsh_ensmbl_entrz, hsh_entrz_human, hsh_human_entrz = {}, {}, {}, {}
	
	for line in open(BASE + "/Data/Human/entrz_ensmbl_full.txt"):
		words = line.rstrip().split("\t")
		hsh_entrz_ensmbl[words[0]] = words[1]
		hsh_ensmbl_entrz[words[1]] = words[0]
	
	for line in open(BASE + "/Data/Human/name_entrz_full.txt"):
		words = line.rstrip().split("\t")
		hsh_human_entrz[words[0]] = words[1]
		hsh_entrz_human[words[1]] = words[0]
		
	print(f"len(hsh_human_entrz) = {len(hsh_human_entrz)}")
	
def get_gene_name_from_ensmbl(e):
	if e in hsh_ensmbl_entrz and hsh_ensmbl_entrz[e] in hsh_entrz_human:
		return hsh_entrz_human[hsh_ensmbl_entrz[e]]
	else:
		return ""

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def read_human_input_files(bpath, in_bin_size):
	global BASE, is_human, bin_size, chr_map, bin_map, nbins, chr_ids, chr_ids_to_names, chr_names_to_ids, chr_length, centromere_bins, rbm20_genes, rbm20_bins

	BASE                      = bpath
	is_human                  = True
	bin_size                  = in_bin_size
	(chr_ids, chr_ids_to_names, chr_names_to_ids) = define_human_chr_ids()
	(chr_map, bin_map, nbins) = read_bin_map(BASE + "/Data/maps/human/bin_map_" + str(bin_size) + ".bed")
	chr_length                = read_chr_length(BASE + "/Data/Human/hg38_chr_lengths.txt")
	centromere_bins           = read_centromeres(BASE + "/Data/Human/centromeres.txt", 5)
	(rbm20_genes, rbm20_bins) = read_RBM20_bins(BASE + "/Data/Human/RBM20_targets.txt")

	return (chr_map, bin_map, nbins, chr_ids, chr_ids_to_names, chr_names_to_ids, chr_length, centromere_bins, rbm20_genes, rbm20_bins)


def read_plasmo_input_files(bpath, in_bin_size):
	global BASE, is_human, bin_size, chr_map, bin_map, nbins, chr_ids, chr_ids_to_names, chr_names_to_ids, chr_length, centromere_bins, virulence_bins

	BASE                      = bpath
	is_human                  = False
	bin_size                  = in_bin_size
	(chr_ids, chr_ids_to_names, chr_names_to_ids) = define_plasmo_chr_ids()
	(chr_map, bin_map, nbins) = read_bin_map(BASE + "/Data/maps/plasmo/bin_map_" + str(bin_size) + ".bed")
	chr_length                = read_chr_length(BASE + "/Data/Plasmo/chrom_lengths.txt")
	centromere_bins           = read_centromeres(BASE + "/Data/Plasmo/centromeres.txt", 5)
	virulence_bins            = read_virulence_genes(BASE + "/Data/Plasmo/virulence_genes.txt")
	

	return (chr_map, bin_map, nbins, chr_ids, chr_ids_to_names, chr_names_to_ids, chr_length, centromere_bins, virulence_bins)



if __name__ == "__main__":
    pass