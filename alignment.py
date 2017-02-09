import re
from collections import defaultdict

def get_phrase_split(phrase):
    phrase_splitted = re.split("(\S+ \(\{[0-9 ]*\}\))", phrase)
    phrase_splitted = [ item.strip() for item in phrase_splitted \
                        if item != " " and item != "" ]
    phrase_splitted = [ re.match(r"(\S+) (\(\{[0-9 ]*\}\))", item) \
                          .group(1, 2) for item in phrase_splitted ]
    phrase_splitted = [ (item[0], int(s)) for item in phrase_splitted \
                        for s in item[1].strip("{()}").split() ]
    return phrase_splitted

def get_alignments(fe_phrase, ef_phrase):
    fe_phrase_splitted = get_phrase_split(fe_phrase[1])
    fe_alignment = [ (y, ef_phrase[0].index(x)+1) for (x, y) in  fe_phrase_splitted ]

    ef_phrase_splitted = get_phrase_split(ef_phrase[1])
    ef_alignment = [ (y, fe_phrase[0].index(x)+1) for (x, y) in  ef_phrase_splitted ]

    return fe_alignment, ef_alignment

def grow_diag(alignment, fe_len, ef_len, aligned, union):
    neighbours = [ (-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1) ]
    prev_len = len(alignment) - 1
    
    # repeat until new points appear
    while prev_len < len(alignment):
        for e in range(1, fe_len+1):
            for f in range(1, ef_len+1):
                if (e, f) in alignment:
                    for neighbour in neighbours:
                        neighbour = tuple(i + j for i, j in zip((e, f), neighbour))
                        e_new, f_new = neighbour
                        if (e_new not in aligned and f_new not in aligned) \
                        and neighbour in union:
                            alignment.add(neighbour)
                            aligned['e'].add(e_new)
                            aligned['f'].add(f_new)
                            prev_len += 1

    return alignment

def final_and(alignment, fe_len, ef_len, aligned, init_align):
     # Add those points are not included in intersection 
     # after checking if can be added

    for e_new in range(1, fe_len+1):
        for f_new in range(1, ef_len+1):
            if (e_new not in aligned and f_new not in aligned
                and (e_new, f_new) in init_align):
                alignment.add((e_new, f_new))
                aligned['e'].add(e_new)
                aligned['f'].add(f_new)


def do_alignment(fe_align, ef_align, fe_sent_len, ef_sent_len):
    fe_align = [ tuple(reversed(x)) for x in fe_align ]
    alignment = set(ef_align).intersection(set(fe_align))
    union = set(ef_align).union(set(fe_align))

    aligned = defaultdict(set)
    for i, j in alignment:
        aligned['e'].add(i)
        aligned['j'].add(j)

    alignment = grow_diag(alignment, fe_sent_len, ef_sent_len, aligned, union)
    final_and(alignment, fe_sent_len, ef_sent_len, aligned, fe_align)
    final_and(alignment, fe_sent_len, ef_sent_len, aligned, ef_align)

    return sorted(alignment, key=lambda item: item)
