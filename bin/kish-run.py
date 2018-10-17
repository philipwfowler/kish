#! /usr/bin/env python

import argparse, re

from Bio import SeqIO

from gemucator import gemucator

def identify_gene(location,promoter_length):

    (gene,ref,position) = reference_genome.identify_gene(location,promoter_length=promoter_length)

    if gene is not None:
        return(gene+"_"+ref+str(position))
    else:
        return("unknown")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--kmer",help="the nucleotide kmer we wish to search for")
    parser.add_argument("--promoter_length",type=int,default=100,help="the number of bases upstream of a gene that we will consider to form the promoter")
    parser.add_argument("--exact",action="store_true",help="if specified, only consider EXACT matches with the genbank file")
    parser.add_argument("--genbank_file",help="the path to the reference GenBank file we want to work with. If not specified, the code will load H37rV.gbk from its config/ folder.")
    options = parser.parse_args()

    if options.genbank_file:
        reference_genome=gemucator(genbank_file=options.genbank_file)
        genome=SeqIO.read(options.genbank_file,"genbank")
    else:
        reference_genome=gemucator()
        genome=SeqIO.read("config/H37Rv.gbk","genbank")

    line=""

    # pull out the forward and reverse complement genomes as strings
    forward_genome=str(genome.seq)
    reverse_genome=str(genome.reverse_complement().seq)

    # first let's try for exact matches
    fishing_kmer=re.compile(options.kmer)

    result=fishing_kmer.search(str(forward_genome))
    if result is not None:
        line+=options.kmer+" exactly matches forward starting at genbank location "+str(result.start())
        line+=" encoding "+identify_gene(result.start(),promoter_length=options.promoter_length)+"\n"


    result=fishing_kmer.search(str(reverse_genome))
    if result is not None:
        line+=options.kmer+" exactly matches reverse starting at genbank location "+str(result.start())
        line+=" encoding "+identify_gene(result.start(),promoter_length=options.promoter_length)+"\n"

    if not options.exact:

        # now step through the kmer and allow a single SNP
        for pos in range(len(options.kmer)):

            # identify the base we are going to allow to change
            fuzzy_base=options.kmer[pos:pos+1]

            # build the regular expression
            fishing_kmer=re.compile(options.kmer[:pos]+'[^'+fuzzy_base+"]"+options.kmer[pos+1:],re.IGNORECASE)

            # search the forward genome
            result=fishing_kmer.search(forward_genome)
            if result is not None:
                line+=options.kmer+" matches forward ("+fuzzy_base+"->"+result.group()[pos]+" at pos "+str(pos)+") starting at genbank location "+str(result.start())
                line+=" encoding "+identify_gene(result.start(),promoter_length=options.promoter_length)+"\n"

            # ..and the reverse complement
            result=fishing_kmer.search(reverse_genome)
            if result is not None:
                line+=options.kmer+" matches reverse ("+fuzzy_base+"->"+result.group()[pos]+" at pos "+str(pos)+") starting at genbank location "+str(result.start())
                line+=" encoding "+identify_gene(result.start(),promoter_length=options.promoter_length)+"\n"

    if line:
        print(line)
    else:
        print(options.kmer+" no matches found!")
