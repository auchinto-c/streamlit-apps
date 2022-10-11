import pandas as pd
import streamlit as sl
import altair as alt
from PIL import Image

img = Image.open('images/dna.jpg')

sl.image(img, use_column_width=True)

sl.write("""
# DNA Nucleotide Count Web app

This app counts the nucleotide composition of query DNA.
""")

sl.header('Enter DNA Sequence')

seq_input = '> DNA Query \nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT'

sequence = sl.text_area("Sequence Input", seq_input, height=25)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

sl.write("***")

sl.header('INPUT (DNA Query)')
sequence

sl.header('OUTPUT (Nucleotide Count')

sl.subheader('Get Dictionary')

def nucleotide_count(seq):
    return {
        'A': seq.count('A'),
        'T': seq.count('T'),
        'G': seq.count('G'),
        'C': seq.count('C'),
    }

nu_count = nucleotide_count(sequence)
nu_count

sl.subheader('Description')

sl.write(f'Count for Adenine (A): {nu_count["A"]}')
sl.write(f'Count for Thymine (T): {nu_count["T"]}')
sl.write(f'Count for Guanine (G): {nu_count["G"]}')
sl.write(f'Count for Cytosine (C): {nu_count["C"]}')

sl.subheader('Display Dataframe')

dna_df = pd.DataFrame.from_dict(nu_count, orient='index')
dna_df = dna_df.rename({0:'count'}, axis='columns')
dna_df.reset_index(inplace=True)
dna_df = dna_df.rename({'index':'Nucleotide'}, axis='columns')
dna_df

sl.subheader('Visualization')

plot = alt.Chart(dna_df).mark_bar().encode(x='Nucleotide', y='count')
plot = plot.properties(width=alt.Step(80))

sl.write(plot)