# kish (kmer fishing)

This is a simple Python package designed to allow kmers to be screened against a GenBank file, in this case H37Rv to see if they match.

If they do, the [gemucator](https://github.com/philipwfowler/gemucator) package is used to identify, if possible, the gene affected.

## Installation and pre-requisites

Since gemucator is not in PyPi, you will need to install it as per the instructions in the README on its [GitHub page](https://github.com/philipwfowler/gemucator).

The only other pre-requsite is BioPython, which if not present, should be installed automatically during the below process.

First, clone the repository

```
$ git clone https://github.com/philipwfowler/kish
$ cd kish/
```

Now install either as a simple static package

`$ python setup.py install --user`

or, as a link if you anticipate updating the package via `git pull` frequently (do this way if the package is being developed and changed rapidly)

`$ python setup.py develop --user`

## Usage

Fairly simple, you give it a kmer and it tells you if it can find it

```
$ kish-run.py --kmer CGGGGTTGACCCACAAGCGCCGACTGTCGGC
CGGGGTTGACCCACAAGCGCCGACTGTCGGC exactly matches forward starting at genbank location 761127 encoding rpoB_S441
```

It also considers all single base variants using a regular expression

```
$ kish-run.py --kmer CGGGGTTGACCCACAAGCGCCGACTGTCCGC
CGGGGTTGACCCACAAGCGCCGACTGTCCGC matches forward (C->G at pos 28) starting at genbank location 761127 encoding rpoB_S441
```

If you want to restrict it to exact matches then

```
$ kish-run.py --kmer CGGGGTTGACCCACAAGCGCCGACTGTCCGC --exact
CGGGGTTGACCCACAAGCGCCGACTGTCCGC no matches found!
```

## Future developments

* allow a file containing a kmer-per-line to be specified to increase speed/ease of use
* if a single base has been changed, work out what mutation in the reference genome that corresponds to
* can we think about 2 base changes? Or will that be too slow.
