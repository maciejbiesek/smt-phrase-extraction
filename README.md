# Phrase extraction

Project was created during Statistical Machine Translation at Computer Science, Adam Mickiewicz University.
It parses GIZA++ output format then run grow-diag-final-and algorithm and finally extract possible phrases. It was tested on portuguese-polish languages.

To run:
> python main.py [fe_file] [ef_file]

Both files has to be in GIZA++ format.

For example:
> python main.py data/pt-pl data/pl-pt
