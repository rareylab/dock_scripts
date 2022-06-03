# DOCK Scripts

A collection of scripts used to automated docking and de novo functionality of DOCK 6.9. To use the scripts
the `config.ini` must be edited with paths to appropriate binaries (mostly included in a DOCK source distribution). The
only python requirement should be python 3. The scripts have been teste with Python 3.6.10.

Tests have been provided in `tests/` and can be executed with:

```bash
python -m unittest tests
```

Config files for docking can be found in `/templates` and largely derived from DOCK publications:

W. J. Allen et al., “DOCK 6: Impact of new features and current docking performance,” J Comput Chem, vol. 36, no. 15,
Art. no. 15, 2015, doi: https://doi.org/10.1002/jcc.23905.

W. J. Allen, B. C. Fochtman, T. E. Balius, and R. C. Rizzo, “Customizable de novo design strategies for DOCK:
Application to HIVgp41 and other therapeutic targets,” J Comput Chem, vol. 38, no. 30, pp. 2641–2663, 2017,
doi: https://doi.org/10.1002/jcc.25052.

Template variables set by the scripts at runtime are in curly braces, for example:

```
atom_in_anchor          {anchor}
```

All scripts in the top level directory have command line interfaces. Examples on how to use the python classes can be
found in the tests.

## Pipelining

The main underlying design concept was incremental pipeline. Single pipeline elements, usually calling one particular
commandline tool, do input and output checks to see whether the expected results already exist. If they do they are not
recalculated them unless forced. Especially preparing receptors can be tedious so this kind of incremental approach
becomes necessary.

## Lessons Learned

1. Proteins with more than 9999 atoms cannot be processed with sphgen. This is why we need to create active sites.
2. Several binaries have problems with path length. Some will cut off input paths beyond 80 characters. Keep this in
   mind when specifiying paths. Many commandline calls are performed in the output directories to minimize path length.
3. On the other hand some binaries __require__ absolute paths because they ignore the current working directory.
