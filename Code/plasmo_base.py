import numpy as np
import os
import sys
import random
import time
import multiprocessing as mp





# --------------------------------------------------------------------------- #
# Read Inputs
# --------------------------------------------------------------------------- #



def read_PePr_peaks(fname):
	pepr_peaks = []
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		peak = {}
		peak["chr"]   = words[0]
		peak["start"] = int(words[1])
		peak["end"]   = int(words[2])
		peak["pval"]  = float(words[7])
		peak["FDR"]   = float(words[8])
		peak["name"]  = words[3]
		peak["pval10"]= -np.log10(float(words[7]))
		peak["width"] = peak["end"] - peak["start"]
		
		if peak["chr"] == "Pf_M76611" or peak["chr"] == "Pf3D7_API_v3":
			continue
		
		pepr_peaks.append(peak)
	
	return pepr_peaks
		
def read_macs_peaks(fname):
	macs_peaks = []
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		peak = {}
		peak["chr"]   = words[0]
		peak["start"] = int(words[1])
		peak["end"]   = int(words[2])
		peak["pval"]  = pow(10,-float(words[6]))
		peak["name"]  = words[3]
		
		if peak["chr"] == "Pf_M76611" or peak["chr"] == "Pf3D7_API_v3":
			continue
			
		macs_peaks.append(peak)
	
	return macs_peaks
		


def read_bed_file(fname):
	reads = []
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		read = {}
		
		read["chr"]   = words[0]
		read["start"] = int(words[1])
		read["end"]   = int(words[2])
		read["name"]  = words[3]
		
		reads.append(read)
	
	return reads





def read_peak_heights(peaks, fname):
	for line in open(fname):
		words = line.rstrip().split("\t")
		for peak in peaks:
			if peak["name"] == words[0]:
				peak["height"] = float(words[1])
				peak["summit"] = int(words[2])




def count_reads_overlapping_peaks(peaks, reads):
	margin = 0
	for read in reads:
		for peak in peaks:
			if (read["chr"] == peak["chr"]) and (read["start"] <= peak["end"] + margin) and (read["end"] + margin >= peak["start"]):
				if "num_reads" in peak:
					peak["num_reads"] += 1
				else:
					peak["num_reads"] = 0


	for peak in peaks:
		print(f"{peak['num_reads']}")


def read_depth_file(fname):
	depth_per_chr, total_depth = {}, 0
	for line in open(fname):
		words = line.rstrip().split("\t")
		
		if words[0] not in depth_per_chr:
			depth_per_chr[words[0]] = []
			depth_per_chr[words[0]].append(0) # take care of zero index
			
		depth_per_chr[words[0]].append(int(words[2]))
		total_depth += int(words[2])
	
	print(f"total_depth = {total_depth}")
	return depth_per_chr



# calculate peak height given a depth file
def calculate_peak_height(peaks, depth):
	for peak in peaks:
		peak["height"] = max([depth[peak["chr"]][i] for i in range(peak["start"], peak["end"] + 1)])





def calculate_automatically_peak_height(file_names, peaks, heights_file_name):
	# read the relevant bed files to get sequencing depth for normalization
	norm_values = [1000000.0/(sum([1 for line in open(f"{P}../Outputs/bams/{fn}_filtered.bed")])) for fn in file_names ]
	
	# read the depth files
	depths = [read_depth_file(f"{P}../Outputs/bams/{fn}_filtered_depth.txt") for fn in file_names ]
	
	# calculate the normalized height and the index of the summit 
	for peak in peaks:	
		heights = [sum([depths[j][peak["chr"]][i]*norm_values[j] for j in range(len(file_names))]) for i in range(peak["start"], peak["end"] + 1)]
		peak["height"] = max(heights)
		peak["summit"] = heights.index(peak["height"])
	
	# write them down
	write_peaks_raw_height(peaks, heights_file_name)
	
	

def write_peaks_raw_height(peaks, extra_name=""):
	fo = open(f"{T}peaks_heights_{extra_name}.txt", "w")
	for peak in peaks:
		fo.write(f"{peak['name']}\t{peak['height']}\t{peak['start'] + peak['summit']}\n")




def sort_peaks_by(peaks, sort_by):
	return [x[0] for x in sorted([[peak, peak[sort_by]] for peak in peaks], key=lambda x: x[1], reverse=True)]



def get_tallest_peaks(peaks, depth1, depth2, fname):
	calculate_peak_height2(peaks, depth1, depth2)
	
	sorted_peaks = sort_peaks_by(peaks, "height")
	
	fo = open(f"{T}{fname}.bed", "w")
	for peak in sorted_peaks:
		fo.write(f"{peak['chr']}\t{peak['start']}\t{peak['end']}\t{peak['name']}\t{peak['height']}\n")
	fo.close()
	
	fo = open(f"{T}{fname}_summits.bed", "w")
	for peak in sorted_peaks:
		fo.write(f"{peak['chr']}\t{peak['summit']}\t{peak['summit']}\t{peak['name']}\t{peak['height']}\n")







def plot_peak_height_v_distance_to_chr_end(peaks, extra_name=""):
	fo = open(f"{T}h_{extra_name}.txt", "w")
	for peak in peaks:
		if peak["height"] < 250  and random.random() < 0.3:
			pass
		
		dist = min((peak["start"] + peak["summit"]), (chr_length[peak["chr"]] - (peak["start"] + peak["summit"])))
		dist_r = float(dist)/chr_length[peak["chr"]]
		fo.write(f"{peak['height']}\t{dist}\t{dist_r}\t{peak['name']}\n")







def peaks_intersect(peaks1, peaks2):
	print(f"len(peaks1) = {len(peaks1)}")
	print(f"len(peaks2) = {len(peaks2)}")
	
	overlapping = 0
	margin = 0
	
	for peak1 in peaks1:
		for peak2 in peaks2:
			if (peak1["chr"] == peak2["chr"]) and (peak1["start"] < peak2["end"] + margin) and (peak1["end"] + margin > peak2["start"]):
				overlapping += 1
				peak1["overlap"] = peak2["name"]
				peak2["overlap"] = peak1["name"]

	print(f"overlapping = {overlapping}")





def explore_peak_intersect():
	fname1 = f"{P}../Outputs/TARE_PePr/peprTARE_Schizont__PePr_peaks.bed"
	#fname2 = f"{P}../Outputs/TARE_PePrSharp/peprTARE_Schizont__PePr_peaks.bed"
	fname2 = f"{P}../Outputs/TARE_PePrSharp/peprTARE_4tRNA2Schizont__PePr_peaks.bed"
	fname2 = f"{P}../Outputs/TARE_PePrSharp/peprTARE_4tRNA__PePr_peaks.bed"
	
	#fname1 = f"{fname1}.passed.boundary_refined"
	#fname2 = f"{fname2}.passed.boundary_refined"

	peaks1  = read_PePr_peaks(fname1)
	peaks2  = read_PePr_peaks(fname2)
	
	fname2 = f"{P}../Outputs/macsTARE/macsTARE_4tRNA_peaks.narrowPeak"
	peaks2  = read_macs_peaks(fname2)
	
	peaks_intersect(peaks1, peaks2)



def explore_peak_dist_v_height():
	depth1       = read_depth_file(f"{P}../Data/flowcell939_lane1_pair1_TCCACGTT_TAREChIRP_filtered_depth.txt")
	depth2       = read_depth_file(f"{P}../Data/flowcell954_lane1_pair1_TAGCTTAT_TARE_rep3_filtered_depth.txt")


	
	
	fname1 = f"{P}../Outputs/macsTARE/macsTARE_4tRNA_peaks.narrowPeak"
	peaks = read_macs_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"macsTARE_4tRNA_peaks")
	write_peaks_raw_height(peaks,"macsTARE_4tRNA_peaks")
	
	
	fname1 = f"{P}../Outputs/macsTARE/macsTARE_4tRNA2Schizont_peaks.narrowPeak"
	peaks = read_macs_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"macsTARE_4tRNA2Schizont_peaks")
	write_peaks_raw_height(peaks,"macsTARE_4tRNA2Schizont_peaks")
	
	
	
	
	fname1 = f"{P}../Outputs/TARE_PePrSharp/peprTARE_4tRNA2Schizont__PePr_peaks.bed"
	peaks = read_PePr_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"peprTARE_4tRNA2Schizont_Sharp")
	write_peaks_raw_height(peaks,"peprTARE_4tRNA2Schizont_Sharp")
	
	
	fname1 = f"{P}../Outputs/TARE_PePr/peprTARE_4tRNA2Schizont__PePr_peaks.bed"
	peaks = read_PePr_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"peprTARE_4tRNA2Schizont")
	write_peaks_raw_height(peaks,"peprTARE_4tRNA2Schizont")
	
	
	fname1 = f"{P}../Outputs/TARE_PePr/peprTARE_Schizont__PePr_peaks.bed"
	peaks = read_PePr_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"peprTARE_Schizont")
	write_peaks_raw_height(peaks,"peprTARE_Schizont")
	
	
	fname1 = f"{P}../Outputs/TARE_PePr/peprTARE_4tRNA__PePr_peaks.bed"
	peaks = read_PePr_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"peprTARE_4tRNA")
	write_peaks_raw_height(peaks,"peprTARE_4tRNA")
	
	
	fname1 = f"{P}../Outputs/TARE_PePrSharp/peprTARE_Schizont__PePr_peaks.bed"
	peaks = read_PePr_peaks(fname1)
	calculate_peak_height2(peaks, depth1, depth2)
	#plot_peak_height_v_distance_to_chr_end(peaks,"peprTARE_Schizont_Sharp")
	write_peaks_raw_height(peaks,"peprTARE_Schizont_Sharp")
	
	
# --------------------------------------------------------------------------- #




# --------------------------------------------------------------------------- #
# READ GFF and 5'3'UTRs
# --------------------------------------------------------------------------- #


def read_gff():
	genes, units, exons, introns = {}, [], [], []
	
	for line in open(f"{P}../Data/PlasmodiumGenome/PlasmoDB-45_Pfalciparum3D7.gff"):
		if line[0] == "#": continue
		
		words = line.rstrip().split("\t")
		
		unit  = {}
		unit["name"]    = words[8].split(";")[0].replace('ID=','')
		unit["chr"]     = words[0]
		unit["start"]   = int(words[3])
		unit["end"]     = int(words[4])

		
		if words[2] == "exon":
			unit["type1"] = "exon"
			exons.append(unit)
			
		if words[2] == "gene":
			strand = words[6]
			unit["strand"] = strand
			
			if len(exons) == 0: continue
			
			# add introns
			for i in range(0, len(exons) - 1):
				intron = {}
				intron["name"]    = f"{exons[i]['name'].replace('exon_','intron_')}"
				intron["chr"]     = exons[i]["chr"]
				intron["start"]   = exons[i]["end"] + 1
				intron["end"]     = exons[i+1]["start"] - 1
				intron["type1"]    = "intron"
			
				introns.append(intron)
			
			# if more than 3 exons for the given gene, do annotate with first/last
			if len(exons) > 2: 	
				if strand == "+": 
					exons.reverse()
					introns.reverse()
				
				exons[0]["type2"] = "first_exon"
				exons[-1]["type2"] = "last_exon"
				for i in range(1, len(exons) - 1):
					exons[i]["type2"] = "internal_exon"
			
				introns[0]["type2"] = "first_intron"
				introns[-1]["type2"] = "last_intron"
				for i in range(1, len(introns) - 1):
					introns[i]["type2"] = "internal_intron"
				
			# add them to the big data struct
			#genes.append(unit)
			genes[unit["name"]] = unit
			for exon in exons:
				units.append(exon)
			for intron in introns:
				units.append(intron)
			exons = []
			introns = []
			

	return (genes,units)



def read_53utr(x):
	utrs = []
	for line in open(f"{P}../Data/PlasmodiumGenome/53utr/{x}utr.txt"):
		if line[0] == "#": continue
		
		words = line.rstrip().split("\t")
		unit  = {}
		unit["name"]    = "empty"
		unit["chr"]     = words[0]
		unit["start"]   = int(words[3])
		unit["end"]     = int(words[4])
		unit["type1"]   = f"{x}UTR"
		
		utrs.append(unit)
	
	print(f"len(utrs) = {len(utrs)}")
	return utrs


def get_unit_annotations():
	(genes,units) = read_gff()
	
	for utr in read_53utr(3):
		units.append(utr)
	
	for utr in read_53utr(5):
		units.append(utr)
	
	
	
	h_overlap = {}
	h_overlap["exon"] = 0; h_overlap["intron"] = 0; h_overlap["5UTR"] = 0; h_overlap["3UTR"] = 0; h_overlap["none"] = 0;
	for unit in units:
		h_overlap[unit["type1"]] += (unit["end"] - unit["start"])
	normalize_hash(h_overlap)
	print(f"h_overlap = {h_overlap}")
	
	return (genes,units)
	


def my_segtool(peaks, units):
	h_overlap = {}
	h_overlap["exon"] = 0; h_overlap["intron"] = 0; h_overlap["5UTR"] = 0; h_overlap["3UTR"] = 0; h_overlap["none"] = 0; 
	
	count = 0
	for peak in peaks:
		count_overlap2(peak, units, h_overlap)
		count += 1
		if count > 0.1*len(peaks):
			break
		
	normalize_hash(h_overlap)
	print(f"h_overlap = {h_overlap}")
	
	fo = open(f"{T}seg.txt", "w")
	for k in h_overlap:
		fo.write(f"{k}\t{h_overlap[k]}\n")
	

def normalize_hash(h):
	s = sum([h[k] for k in h])
	for k in h:
		h[k] = h[k]/s




def count_overlap(peak, units, h_overlap):
	total_overlap = 0
	
	for unit in units:
		if unit["chr"] != peak["chr"]: continue
		if peak["start"] > unit["end"] or peak["end"] < unit["start"]: continue
		overlap = (min(peak["end"], unit["end"]) - max(peak["start"], unit["start"]))/peak["width"]
		
		if overlap > 0:
			h_overlap[unit["type1"]] += overlap
			total_overlap += overlap
			
	
	h_overlap["none"] += (1 - total_overlap)








def explore_peak_segtool():
	fname = f"{P}../Outputs/TARE_PePr/peprTARE_Schizont__PePr_peaks.bed"
	hname = f"{P}../Outputs/PeakHeights/peaks_heights_peprTARE_Schizont.txt"
	lnc = "TARE"
	
	
	
	lnc = "lnc271__PePr_chip1_peaks"	
	fname = f"{P}../Outputs/peprZALL/{lnc}.bed"
	hname = f"{P}../Outputs/PeakHeights/peaks_heights_{lnc}.txt"
	
	
	peaks = read_PePr_peaks(fname)
	read_peak_heights(peaks, hname)
	

	sorted_peaks = sort_peaks_by(peaks, "height")
	
	print_sorted_bed(sorted_peaks, lnc)



	
	(genes,units) = get_unit_annotations()
	
	my_segtool(sorted_peaks, units)


def print_sorted_bed(sorted_peaks, lnc):
	fo = open(f"{T}{lnc}_top.bed", "w")
	for i in range(0,int(0.1*len(sorted_peaks))):
		peak = sorted_peaks[i]
		fo.write(f"{peak['chr']}\t{peak['start']}\t{peak['end']}\t{peak['height']}\n")




# find the nearest gene to a given peak
def find_nearest_genes(peaks, genes):
	for peak in peaks:
		find_nearest_gene0(peak, genes)

def find_nearest_gene0(peak, genes):
	peak["min_dist_gene"] = 1000000
	for gene_name, gene in genes.items():
		if gene["chr"] != peak["chr"]: continue
		
		dist = min(abs(gene["start"] - peak["summit"]), abs(gene["end"] - peak["summit"]))
		
		if dist < peak["min_dist_gene"]:
			peak["gene"] = gene
			peak["min_dist_gene"] = dist



def find_nearest_gene(peak, genes):
	z = sorted([(min(abs(gene["start"] - peak["summit"]), abs(gene["end"] - peak["summit"])), gene) for gene in [gene for gene in genes.values() if gene["chr"] == peak["chr"]]], key=lambda x: x[0], reverse=False)
	peak["gene"], peak["min_dist_gene"] = z[0][1], z[0][0]
	





# retutn True if the given coordinate is within the given peak
def overlap_coordinate_peak(i, peak):
	if peak["start"] <= i and peak["end"] >= i:
		return True
	return False





def entry_segplot_new():
	lnc_name = "lnc1494"
	lnc = f"{lnc_name}__PePr_chip1_peaks"	
	fname = f"{P}../Outputs/peprZALL/{lnc}.bed"
	hname = f"{P}../Outputs/PeakHeights/peaks_heights_{lnc}.txt"
	
	
	peaks = read_PePr_peaks(fname)
	read_peak_heights(peaks, hname)
	
	# get the top 25% of tallest peaks
	sorted_peaks = sort_peaks_by(peaks, "height")[0:(int(0.25*len(peaks)))]


	
	
	(genes,units) = get_unit_annotations()
	
	find_nearest_genes(peaks, genes)

	segplot_new(sorted_peaks, genes, lnc_name)


def segplot_new(peaks, genes, lnc_name):
	arr_density_AGGREGATE = np.zeros((1,3000))[0]
	print(f"len(peaks) = {len(peaks)}")
	
	for peak in peaks:
		arr_density = [0]*3000
		gene = peak["gene"]

		# 5' end
		arr_coordiantes = list(range((gene["start"] - 1000), gene["start"]))
		for i in range(1000):
			if overlap_coordinate_peak(arr_coordiantes[i], peak):
				arr_density[i] += 1
		

		# 3' end
		arr_coordiantes = list(range((gene["end"]), (gene["end"] + 1000)))
		for i in range(1000):
			if overlap_coordinate_peak(arr_coordiantes[i], peak):
				arr_density[i + 2000] += 1
		
		
		# discrete decile gene length overlap
		gene_length = abs(gene["end"] - gene["start"])
		gene_tenth  = int(gene_length/10)
		arr_gene_body = np.zeros((1,10))[0]
		
		for j in range(10):
			for i in range((gene["start"] + j*gene_tenth), (gene["start"] + (j + 1)*gene_tenth)):
				if overlap_coordinate_peak(i, peak):
					arr_gene_body[j] += 1
							
		for k in range(1000):
			arr_density[k + 1000] += float(arr_gene_body[int(k/100)])/gene_tenth

		if gene["strand"] == "-":
			arr_density.reverse()
			
		for i in range(3000):
			arr_density_AGGREGATE[i] += arr_density[i]


	arr_density = arr_density_AGGREGATE/len(peaks)
	
	fo = open(f"{T}seg.txt", "a")
	names = ['5 end', 'gene body', '3 end']
	for i in range(3000):
		fo.write(f"{i}\t{arr_density[i]}\t{names[int(i/1000)]}\t{lnc_name}\n")
		

# --------------------------------------------------------------------------- #
# Main Executable
# --------------------------------------------------------------------------- #

H = "/net/noble/vol1/home/borislav/"
P = f"{os.path.dirname(os.path.abspath(__file__))}/"
T = f"{P}../Temp/"

OUTPUTS = f"{P}../Outputs/"

if P[0:10] == "/net/noble":
	P = "/net/noble/vol1/home/borislav/proj/2021_borislav_plasmo-chirp-new/Code/"
	T = f"{P}../Temp/"



from base import *


def read_input_data():
	global chr_map, bin_map, nbins, chromosome_names, centromere_bins, virulence_bins, chr_names_to_ids

	(chr_map, bin_map, nbins, chr_ids, chr_ids_to_names, chr_names_to_ids, chr_length, centromere_bins, virulence_bins) = read_plasmo_input_files("/Users/bhristov6/Desktop/Code/base", 10000)


def get_peaks_25(lnc):	
	peaks = []

	for line in open(f"{P}../Outputs/peaks_25/{lnc}.txt"):
		words = line.rstrip().split("\t")
		
		peak = {}
		peak["chr"]   = words[0]
		peak["start"] = int(words[1])
		peak["end"]   = int(words[2])
		peak["height"]= float(words[4])
		
		peaks.append(peak)
		
	return peaks
	

def entry_bed():
	fname = "flowcell939_lane1_pair1_GTAAGGTG_Ch9ChIRP_filtered.bed"
	
	dname = f"{P}../Outputs/beds3/"
	fname = f"{dname}{fname}"
	

	read_bed_raw_peaks(fname, get_peaks_25("ch9"))
	
	



def read_bed_raw_peaks(fname, peaks):
	arr = [0]*nbins
	peak_bins = []
	for peak in peaks:
		peak_bins.append(get_bin_from_chr_loc(chr_names_to_ids[peak['chr']], int((peak['start'] + peak['end'])/2)))
		if len(peak_bins) > 18: break
	
	
	for line in open(fname):
		words = line.rstrip().split("\t")
		chr = words[0]
		mid = int(int(words[2]) + int(words[1]))/2
		
		if chr == 'Pf3D7_API_v3' or chr == "Pf_M76611": continue
		bin = get_bin_from_chr_loc(chr_names_to_ids[chr], mid)
		arr[bin] += 1
		
	all_reads = sum([i for i in arr])
	max_el = max(arr)
	print(f"max_el = {max_el}")
	arr = [float(i)/max_el for i in arr]
	
	for i in range(len(arr)):
		if arr[i] == 0:
			print(f"zero found at i = {i}")
			arr[i] = (arr[i-1]+arr[i+1])/2


	
	fo = open(f"{T}l.txt", "w")
	for i in range(len(arr)):
		if i in peak_bins:
			color = "peak"
		else:
			color = "notso"
		fo.write(f"{i}\t{arr[i]}\t{color}\n")


read_input_data()
entry_bed()

#entry_segplot_new()

#produce_peaks()

#entry_height()


#var_genes = read_virulence_genes()

#explore_peak_intersect()
#explore_peak_dist_v_height()
#extract_peaks()


