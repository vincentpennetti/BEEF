# BEEF
BEEF is a Base Editor Enrichment Function intended to filter CRISPR targets predicted by Doench et al. (2016) into a the subset of targets that can produce premature stop codons with the _Pm_CDA1 dCas9 base editor. Current parameters are set to filter targets that can induce a stop codon between -17 and -19 upstream of the PAM (inclusive) of 20nt target sequences.


To run BEEF:

- Predict N(20)NGG CRISPR sites with Doench _et al._ (2016) activity scoring in Geneious Prime. Export all predicted annotations to .csv 
- Run BEEF script, provide CDS (without stop codon), CDS direction (1 for forward, 0 for reverse), and navigate to the file containing the annotations
- BEEF will then output candidate targets and their respective PAMs to a .txt file in the directory where BEEF is stored
- Return to Geneious Prime and remove all targets absent from BEEF output
- Manually select which target(s) are most viable for your workflow
