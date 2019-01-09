## Hash table benchmarking
A basic library of tools to build, test, and view results of various hash
table types.

### Prerequisites

* make
* gcc and recent g++ (4.3-ish?...(I am use 8.2 with no problems ~Nick))
* boost
* google-sparsehash
* qt

Most of the above can be install via apt-get / rpm / home-brew commands, e.g.,
boost, google-sparsehash, qt4, but in some cases, the full list and versions
of homebrew-core must be made accessible via `brew tap homebrew/cask`.

The individual repositories for a few hash table types not accessible via a
standard package manager call must also be checked out, including:

* array-hash [https://github.com/Tessil/array-hash.git]
* hopscotch-map [https://github.com/Tessil/hopscotch-map.git]
* libcuckoo [https://github.com/nickrose/libcuckoo.git]
* ordered-map [https://github.com/Tessil/ordered-map.git]
* robin-map [https://github.com/Tessil/robin-map.git]
* sparse-map [https://github.com/Tessil/sparse-map.git]
* sparsepp [https://github.com/greg7mdp/sparsepp.git]

These hash table library and includes must be cloned/checked-out in this
directory (e.g., `./hash-table-shootout/libcuckoo`) for the relevant
`-Ilibcuckoo` reference include (and similarly for the other) in the Makefile
to work when compiling.

I have commented out the "standard" hash tables both in the `Makefile` and in
the `bench.py` script that I have been unable to easily find / install. I have
also hard coded a `LOCAL_INCLUDE` path for use with
brew (i.e., `/usr/local/Cellar/`), make sure your include are accessible off of
this base path. There may be other include directories that must be on the
standard or personalize include paths. The missing `ska` and `emilib` hash tables
could be installed, built, and tested, but I don't care about a complete
comparison.


### Running the benchmarks and viewing results

For executing the benchmark tests, run:


    $ make
    $ python bench.py
    $ python make_chart_data.py < output | python make_html.py

Your charts are now in charts.html.

You can tweak some of the values in bench.py to make it run faster at the
expense of less granular data, and you might need to tweak some of the tickSize
settings in charts-template.html.

To run the benchmark at the highest priority possible, do this:

    $ sudo nice -n-20 ionice -c1 -n0 sudo -u $USER python bench.py

You might also want to disable any swap files/partitions so that swapping
doesn't influence performance.  (The programs will just die if they try to
allocate too much memory.)

===============================================================================
### Copyright Information


Written by Nick Welch in 2010.
Forked by Tessil in 2016.
Forked by Nick Roseveare in 2019.
No copyright.  This work is dedicated to the public domain.
For full details, see http://creativecommons.org/publicdomain/zero/1.0/
