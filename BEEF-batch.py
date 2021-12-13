import csv
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


def reverse_complement(sequence):
    """ takes as input a DNA sequence and returns the reverse complement"""
    rev = ""
    for nt in sequence:
        if nt == 'A':
            rev += 'T'
        elif nt == 'T':
            rev += 'A'
        elif nt == 'G':
            rev += 'C'
        elif nt == 'C':
            rev += 'G'
        else:
            raise ValueError("unknown residue in sequence")
    return rev[::-1]
    
# finds the index of the guide
def guide_index_fun(guide, cds):
    """ returns the index of the guide """
    cds_RC = reverse_complement(cds)
    
    if guide in cds:
        guide_index = cds.index(guide)
        match_dir = 1
        
    elif guide in cds_RC:
        guide_index = cds_RC.index(guide)
        match_dir = 0
    else:
        raise ValueError("Guide not found")

    return guide_index, match_dir


# find the editing window for 20mers
def twentyMer_editor(match_dir, target):
    """ Takes as input the cds direction, guide direction, and target
        returns the editing window for a particular target"""
    
    if (match_dir == 1):
        editing_window = [cds.index(target) + 1, cds.index(target) + 4]
    elif (match_dir == 0):
        editing_window = [cds.index(reverse_complement(target)) + 16, cds.index(reverse_complement(target)) + 19]
    else:
        raise ValueError("unknown exception has occurred")
    
    return editing_window


# do the base editing
def base_editing(editing_window, cds_list):
    """ changes all c's in an editing window to t's, returns the edited cds"""
    internal_cds_list = cds_list.copy()
    for x in range(editing_window[0], editing_window[1]):
        if internal_cds_list[x] == 'C':
            internal_cds_list[x] = 'T'

    # re-concatenate the list and generate codons
    re_cat = ''.join(internal_cds_list)
    edited_cds = [re_cat[x:x+3] for x in range(0, len(re_cat),3)]

    return edited_cds

# detect stop codons
def stop_detector(stop_codons, edited_cds):
    """ searches for a stop codon in a provided cds"""
    # check for early stop codon
    for stp in stop_codons:
        if stp in edited_cds:
            return True
    return False


# master function for processing targets
def target_processor(cds, cds_list, target, pam, guide_dir):
    """ the main processing function integrating the above to assess if
        a target is truly viable or not"""
    
    guide_index, match_dir = guide_index_fun(target, cds)

    editing_window = twentyMer_editor(match_dir, target)

    edited_cds = base_editing(editing_window, cds_list)

    return stop_detector(stop_codons, edited_cds)


def main():
    # sequence information
    cds = input("Input your CDS starting with ATG, without stop codon: ")
    cds_list = list(cds)
    cds_codons = [cds[x:x+3] for x in range(0, len(cds),3)]

        
    # C -> T transition candidates
    eligible_targets = ['CAA', 'CAG', 'CGA',] # CCA on the - strand
    stop_codons = ['TAA', 'TAG', 'TGA']
    
    # obtain the file and parse out the important
    Tk().withdraw()
    filePath = askopenfilename()

    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        csvrows =  []    
        for row in reader:
            csvrows.append(row)
        file.close()

    stripped_list = []

    f = open((filePath.split('/')[-1]).split('.')[0] + '_KO_candidates.txt', "x")
    f.write('       Target        PAM\n-------------------- ---\n')
    for row in csvrows[1:]:
        target = row[12]
        pam = row[10]
        direction = row[4]

        if direction == "forward":
            target_dir = 1
        elif direction == "reverse":
            target_dir= 0
        else:
            raise ValueError("invalid target direction")
        
        if target_processor(cds, cds_list, target, pam, target_dir):
            f.write(target + ' ' + pam + '\n')
            stripped_list.append([target, pam])

    f.close()

#######################################

if __name__ == "__main__":
    main()
    
    


