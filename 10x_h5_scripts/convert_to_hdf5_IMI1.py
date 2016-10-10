import subprocess
import pandas as pd
import tables    # users must go through downloading this and HDF5 software---put into documentation
from tables import *
import numpy as np
#import numexpr as ne # also, *must* have Cython installed

import os
os.chdir("/gpfs/commons/home/biederstedte-934/data/Maciejowski2015/10x/IMI-1-10X-chromium/PHASER_SVCALLER_CS/PHASER_SVCALLER/ATTACH_PHASING/fork0/files/")

bam_path = "/gpfs/commons/home/biederstedte-934/data/Maciejowski2015/10x/IMI-1-10X-chromium/PHASER_SVCALLER_CS/PHASER_SVCALLER/ATTACH_PHASING/fork0/files/phased_possorted_bam.bam"

bxbam_name = "IMI-1-10X-chromium_phased_possorted_bam.h5"

col1 = "QNAME"
col2 = "BX"
columns_to_index = [col1, col2]   # list columns to index now, only

bxbam_columns = ["QNAME", "FLAG", "RNAME", "POS", "MAPQ", "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL", "BX"]


from tables import *
class Barcoded_bam(IsDescription):
    QNAME = StringCol(64)
    FLAG  = Int16Col()
    RNAME = StringCol(64)
    POS   = Int32Col()
    MAPQ  = Int8Col()
    CIGAR = StringCol(64)
    RNEXT = StringCol(64)
    PNEXT = Int32Col()
    TLEN  = Int32Col()
    SEG   =  StringCol(256)
    QUAL  = StringCol(256)
    BX    = StringCol(64)

# 'open_file' comes from 'from tables import *'

# Open a file in "w"rite mode
h5file = open_file(bxbam_name, mode = "w")

#create group
group = h5file.create_group("/", "bam_table")

table = h5file.create_table(group, 'bam_fields',  Barcoded_bam, "table of 10x bam field values")

bxbam = table.row

task = subprocess.Popen("samtools view "+ bam_path, shell=True,  stdout=subprocess.PIPE)
for i, line in enumerate(l.decode(errors='ignore') for l in task.stdout):  # decode binary
    toks = line.split()   # split on all whitespace
    newline = dict(zip(bxbam_columns, toks))  # dictionary of 11 mandatory fields
    toks12 = toks[12:]  # rest of lines
    newline1 = dict(item.split(':', 1) for item in toks12) # 2nd dictionary for rest of field:value's
    merged_dict = newline.copy() # first dictionary...best method for Python pre-3.5
    merged_dict.update(newline1) # ...merged with second dictionary
    bxbam["QNAME"] = merged_dict.get("QNAME", "NaN")
    bxbam["FLAG"]  = merged_dict.get("FLAG", "NaN")
    bxbam["RNAME"]  = merged_dict.get("RNAME", "NaN")
    bxbam["POS"]  = merged_dict.get("POS", "NaN")
    bxbam["MAPQ"]  = merged_dict.get("MAPQ", "NaN")
    bxbam["CIGAR"]  = merged_dict.get("CIGAR", "NaN")
    bxbam["RNEXT"]  = merged_dict.get("RNEXT", "NaN")
    bxbam["PNEXT"]  = merged_dict.get("PNEXT", "NaN")
    bxbam["TLEN"]  = merged_dict.get("TLEN", "NaN")
    bxbam["SEG"]  = merged_dict.get("SEG", "NaN")
    bxbam["QUAL"]  = merged_dict.get("QUAL", "NaN")
    bxbam["BX"]  = merged_dict.get("BX", "NaN")
    table.flush()

h5file.close()


