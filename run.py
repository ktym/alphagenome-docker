import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.runtime_version")

from alphagenome import colab_utils
from alphagenome.data import gene_annotation
from alphagenome.data import genome
from alphagenome.data import transcript as transcript_utils
from alphagenome.interpretation import ism
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers
from alphagenome.visualization import plot_components
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

print("\nAvailable Output Types:")
print([output.name for output in dna_client.OutputType])

dna_model = dna_client.create(API_KEY)

if len(sys.argv) < 2:
    print("Usage: python run.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
  dna = f.read()

dna = "".join(dna.split()).upper()  # remove whitespace and ensure uppercase
dna = "".join(base if base in "ACTG" else "N" for base in dna)

thresholds = [2048, 16384, 131072, 524288, 1048576]
dna_len = len(dna)
pad_len = 10000
max_len = thresholds[-1]
if dna_len > max_len:
    dna = dna[:max_len]
    dna_len = len(dna)
for t in thresholds:
  if dna_len <= t - pad_len:
    dna_pad = dna.rjust(dna_len + pad_len, "N").ljust(t, "N")
    print([dna_len, t, len(dna_pad)])
    break

uberon = {
    "Lung": "UBERON:0002048",
    "Brain": "UBERON:0000955",
    "Heart": "UBERON:0000948",
    "Liver": "UBERON:0002107",
}

selected_organs = ["Lung", "Brain", "Liver"]

output = dna_model.predict_sequence(
    sequence=dna_pad,
    requested_outputs=[
        dna_client.OutputType.CAGE,
        dna_client.OutputType.DNASE,
    ],
    ontology_terms=[uberon[organ] for organ in selected_organs],
)

print(f'DNASE predictions shape: {output.dnase.values.shape}')
print(output.dnase.metadata)
dnase = output.dnase.values
dnase_tracks = dnase.shape[1]
colors = plt.cm.tab10.colors
for i in range(dnase_tracks):
    signal = dnase[:, i]
    color = colors[i % len(colors)]  # 色を循環
    plt.plot(
        signal,
        label=selected_organs[i],
        color=color,
        marker='.',
        linestyle='None',
        alpha=0.7,
        markersize=2
    )
plt.legend(loc='upper right')
plt.xlabel("bp")
plt.ylabel("DNASE")
plt.title("Result")
plt.grid(True)
plt.axvline(x=pad_len, color='red', linestyle='--', linewidth=1)
plt.axvline(x=pad_len + dna_len, color='red', linestyle='--', linewidth=1)
plt.savefig("dnase.png", dpi=300, bbox_inches="tight")
plt.show()

print(f'CAGE predictions shape: {output.cage.values.shape}')
print(output.cage.metadata)

"""
interval = genome.Interval(chromosome='chr22', start=35677410, end=36725986)
variant = genome.Variant(
    chromosome='chr22',
    position=36201698,
    reference_bases='A',
    alternate_bases='C',
)

outputs = dna_model.predict_variant(
    interval=interval,
    variant=variant,
    ontology_terms=['UBERON:0001157'],
    requested_outputs=[dna_client.OutputType.RNA_SEQ],
)

plot_components.plot(
    [
        plot_components.OverlaidTracks(
            tdata={
                'REF': outputs.reference.rna_seq,
                'ALT': outputs.alternate.rna_seq,
            },
            colors={'REF': 'dimgrey', 'ALT': 'red'},
        ),
    ],
    interval=outputs.reference.rna_seq.interval.resize(2**15),
    # Annotate the location of the variant as a vertical line.
    annotations=[plot_components.VariantAnnotation([variant], alpha=0.8)],
)
plt.show()
"""
