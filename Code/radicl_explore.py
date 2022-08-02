from hatch import *



# --------------------------------------------------------------------------- #
# Read tags from bed file
# --------------------------------------------------------------------------- #

# reads a bed file of RADICL tags mappings that may NOT BE UNIQUE
# we have obtained those via bowtie after splititng the RADICL reads into tags based on the bridge
# multiple alignments allowed!!!
def read_tags_multuiple_alignment(fname):
	tags = {}
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		# avoid plastids
		if "API" in words[0] or "M" in words[0]:
			continue
		
		# get the read id
		read_id = words[3]
		
		if read_id not in tags:
			tags[read_id] = []
		
		this_alignment = {}
		this_alignment["chr-Pf"] = words[0]
		this_alignment["chr"]    = int(words[0].split("_")[1]) # convert to our chr_id
		this_alignment["start"]  = int(words[1])
		this_alignment["end"]    = int(words[2])
		
		tags[read_id].append(this_alignment)
	
	return tags










# --------------------------------------------------------------------------- #
# Extract the full 151nt sequences that made the final valid pairs
# --------------------------------------------------------------------------- #

def extract(rna_tags, dna_tags):
	fo = open(f"{T}extarcted31.fastq", "w")

	LD = "/net/noble/vol1/home/borislav/proj/Data/LeRochLab/2022-03-RADICL/"
	#LD = "/net/noble/vol1/home/borislav/proj/Data/LeRochLab/2022-05-RADICL/"

	fname = f"{LD}Undetermined_S0_R1_001.fastq.gz"
	#fname = f"{LD}RAD9_S2_R1_001.fastq.gz"

	all_tags = {}
	for tag in rna_tags:
		if tag in dna_tags:
			all_tags[tag] = 1

	print(len(all_tags))

	num_lines, num_found = 0, 0
	with gzip.open(fname,'rt') as f:
		for line in f:
			num_lines += 1
			words = line.rstrip()
			
			# if it is the first line it must be the header
			if num_lines%4 == 1:
				header = words
			
			# if it is the second line then it is the nucleotide sequence
			elif num_lines%4 == 2:
				seq = words
				
			# if it is the third line it must be a '+'
			elif num_lines%4 == 3:
				pass
					
			# if it the fourth line it must be the quality
			elif num_lines%4 == 0:
				qual = words

				# if the read is in our final pairs write it down
				read_id = header.split(" ")[0][1:]
				

				if read_id in all_tags:
					num_found +=1 		
					fo.write(f"{header}\n")
					fo.write(f"{seq}\n")
					fo.write(f"+\n")
					fo.write(f"{qual}\n")
				

			if num_lines < -400000:
				break

	print(f"num_found = {num_found}")








# --------------------------------------------------------------------------- #
# Helper Function
# --------------------------------------------------------------------------- #

# find all tags (with their alignemtns) that overlap a given lncRNA
def find_overlapping_tags(lnc, tags):
	tags_found = []
	
	ZZ_MARGIN = 0
	# for every read (tag)
	for tag in tags:
		# for every aligment of the given tag (read)
		for alignment in tags[tag]:	
			# if they are on the same chromosome
			if alignment['chr-Pf'] == lnc["chr-Pf"]:
				# if there is an overlap
				if alignment["start"] <= (lnc["end"] + ZZ_MARGIN) and alignment["end"] >= (lnc["start"] - ZZ_MARGIN):
					tags_found.append((tag, alignment))
				
	return tags_found





# --------------------------------------------------------------------------- #
# Basic Statistics
# --------------------------------------------------------------------------- #

# print basic statistics
def explore_stats(rna_tags, dna_tags):
	num_proximal, num_trans, num_distal, num_missing_corresponding = 0, 0, 0, 0
	
	# for every rna tag see if there is a corresponding dna tag
	for tag in rna_tags:
		xal = rna_tags[tag][0]
		if tag in dna_tags:
			# for every alignment of that rna tag
			for alignment in dna_tags[tag]:			
				
				if alignment["chr"] == xal["chr"] and abs(alignment["start"] - xal["start"]) < 1000:
					num_proximal += 1
					
				elif alignment["chr"] == xal["chr"]:
					num_distal += 1
					
				elif alignment["chr"] != xal["chr"]:
					num_trans += 1
					
				else:
					raise "can't be here"
			
		else:
			num_missing_corresponding += 1
	
	
	print(f"\n")
	total = num_proximal + num_trans + num_distal
	print(f"total = {total}")
	print(f"num_proximal = {100*num_proximal/total}")
	print(f"num_distal = {100*num_distal/total}")
	print(f"num_trans = {100*num_trans/total}")
	print(f"left with = {num_trans + num_distal}")
	print(f"left with = {round((num_trans + num_distal)*100.0/1314530,2)}%")
	print(f"num_missing_corresponding = {num_missing_corresponding}")



def basic_histogram_reads_mapping(dna_tags):
	fo = open(f"{T}hist.txt", "w")
	for tag in dna_tags:
		fo.write(f"{len(dna_tags[tag])}\tdna\n")
		






# --------------------------------------------------------------------------- #
# Explore lncRNA and RADICL
# --------------------------------------------------------------------------- #

# Base function: Given lncRNA find all tags overlapping with it
def explore_lncRNA(rna_tags, dna_tags, lnc_id="TCONS_00000748"):
	# 0. Read the lnc coordiantes
	lnc = read_lncRNAs(False)[lnc_id]
	print(f"lnc = {lnc}")
	

	# 1. Find all the tags that overlap with the known lnc coordinates
	rna_found = find_overlapping_tags(lnc, rna_tags)
	print(f"found RNA tags overlapping with lncRNA = {len(rna_found)}")
	
	
	# 2. Write down a bed file and array
	fo = open(f"{T}{lnc_id}.bed", "w")
	array, dna_tags_found = [0]*nbins, []
	
	# for every rna tag that overlaps with the lncRNA coordinates
	for (tag, aligns) in rna_found:
		# if there is a corresponding dna tag
		if tag in dna_tags:
			# for every alignment of that dna tag
			for alignment in dna_tags[tag]:
				dna_coord = get_bin_from_chr_loc(alignment["chr"], alignment["start"])
				
				# write it in a bed file
				fo.write(f"{alignment['chr-Pf']}\t{alignment['start']}\t{alignment['end']}\t{tag}\n")

				# count it fractionally in the bin it falls
				array[dna_coord] += 1.0#/len(dna_tags[tag])
			
			# keep track of how many aligments per tag are found
			dna_tags_found.append(len(dna_tags[tag]))
	

	print(f"and corresponding {len(dna_tags_found)} dna tags with mappings = {sum(dna_tags_found)}")
	write_array(array, f"{T}arr.txt")
	


def entry_explore_lncRNAs():
	#for lnc_id in ["TCONS_00000748", "TCONS_00000676", "TCONS_00001124","TCONS_00001687"]:
	#for lnc_id in read_lncRNAs(True):
	for lnc_id in ["TCONS_00000748"]: # this is TARE
		explore_lncRNA(lnc_id)








# --------------------------------------------------------------------------- #
# Create matrix
# --------------------------------------------------------------------------- #

# Given the RADICL data, create the Hi-C like matrix
def create_matrix(rna_tags, dna_tags):
	a = np.zeros((nbins, nbins))

	for rna_tag in rna_tags:
		rna_coord = get_bin_from_chr_loc(rna_tags[rna_tag][0]["chr"], rna_tags[rna_tag][0]["start"])

		if rna_tag in dna_tags:
			for alignment in dna_tags[rna_tag]:
				dna_coord = get_bin_from_chr_loc(alignment["chr"], alignment["start"])

				a[dna_coord][rna_coord] += 1

	np.save(f"{T}m3.npy", a)
	generate_mcool(a, "cm")
	#write_matrix(a, f"{T}matrix3.txt", 0)







# --------------------------------------------------------------------------- #
# Matrix per lncRNA
# --------------------------------------------------------------------------- #

# find which lncRNAs have the most reads so that we can focus on them
def sort_lncRNAs_per_reads(rna_tags, dna_tags):
	lncRNAs = read_lncRNAs(False)

	lnc_sort = []
	for lnc_id in lncRNAs:
		rna_found = find_overlapping_tags(lncRNAs[lnc_id], rna_tags)
		lnc_sort.append([lnc_id, len(rna_found)])
		
	# sort them
	lnc_sort.sort(key=lambda x: int(x[1]), reverse=True)
	
	# write them down
	fo = open(f"{T}sorted_lnc.txt", "w")
	for x in lnc_sort:
		fo.write(f"{x[0]}\t{x[1]}\n")



def matrix_per_lnc(rna_tags, dna_tags):
	# Step 0. Do this once
	# sort_lncRNAs_per_reads(rna_tags, dna_tags)
	
	# Get the lncRNAs with most tags
	lnc_sort = []
	lncRNAs  = read_lncRNAs(False)
	for line in open(f"{T}sorted_lnc.txt"):
		words = line.rstrip().split("\t")
		lnc_sort.append([words[0], int(words[1])])
	

	# Now for the top 100, plot a amtrix
	array = np.zeros((nbins, 100))
	fo_arr = open(f"{T}arr_lnc.txt", "w")
	
	for i in range(100):
		lnc_id = lnc_sort[i][0]
		lnc = lncRNAs[lnc_id]
		rna_found = find_overlapping_tags(lnc, rna_tags)

		# for every rna tag that overlaps with the lncRNA coordinates
		for (tag, aligns) in rna_found:
			# if there is a corresponding dna tag
			if tag in dna_tags:
				# for every alignment of that dna tag
				for alignment in dna_tags[tag]:
					dna_coord = get_bin_from_chr_loc(alignment["chr"], alignment["start"])		

					# count it fractionally in the bin it falls
					array[dna_coord][i] += 1.0#/len(dna_tags[tag])

		# genome tracks
		if i < 10:
			for j in range(nbins):
				if array[j][i] > 0:
					fo_arr.write(f"{j}\t{array[j][i]}\t{lnc_id}\n")

	write_matrix(array, f"{T}lnc_matrix.txt")




# --------------------------------------------------------------------------- #
# Entry Start
# --------------------------------------------------------------------------- #

def entry_start():
	fpath = f"{P}zOuts-OF"
	
	dna_tags = read_tags_multuiple_alignment(f"{fpath}/c_dna_k20.bed")
	rna_tags = read_tags_multuiple_alignment(f"{fpath}/c_rna.bed")
	


	explore_lncRNA(rna_tags, dna_tags)
	create_matrix(rna_tags, dna_tags)
	explore_stats(rna_tags, dna_tags)
	#extract(rna_tags, dna_tags)
	#matrix_per_lnc(rna_tags, dna_tags)






# --------------------------------------------------------------------------- #
# Executable
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
	global bin_size, chr_map, bin_map, nbins
	bin_size = 10000
	(chr_map, bin_map, nbins) = read_fixed_data(bin_size)

	entry_start()
