import os
import matplotlib.pyplot as plt
import numpy as np
from alphagenome.models import dna_client

uberon_map = {
    "Lung": "UBERON:0002048",
    "Brain": "UBERON:0000955",
    "Heart": "UBERON:0000948",
    "Liver": "UBERON:0002107",
}

thresholds = [2048, 16384, 131072, 524288, 1048576]


def analysis(fasta_path, selected_organs, selected_outputs):
    API_KEY = os.environ.get("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY environment variable is not set.")

    with open(fasta_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if lines and lines[0].startswith(">"):
        lines = lines[1:]
    dna = "".join(lines).replace(" ", "").replace("\t", "").replace("\n", "").upper()
    dna = "".join(base if base in "ACTG" else "N" for base in dna)

    dna_len = len(dna)
    pad_len = 10000
    max_len = thresholds[-1]
    if dna_len > max_len:
        dna = dna[:max_len]
        dna_len = len(dna)

    for t in thresholds:
        if dna_len <= t - pad_len:
            dna_pad = dna.rjust(dna_len + pad_len, "N").ljust(t, "N")
            break

    dna_model = dna_client.create(API_KEY)

    requested_outputs = [getattr(dna_client.OutputType, o) for o in selected_outputs if hasattr(dna_client.OutputType, o)]
    ontology_terms = [uberon_map[o] for o in selected_organs if o in uberon_map]

    output = dna_model.predict_sequence(
        sequence=dna_pad,
        requested_outputs=requested_outputs,
        ontology_terms=ontology_terms,
    )

    logs = []
    img_path = None

    if hasattr(output, "dnase"):
        logs.append(f"DNASE predictions shape: {output.dnase.values.shape}")
        logs.append(str(output.dnase.metadata))
        dnase = output.dnase.values
        colors = plt.cm.tab10.colors
        for i in range(dnase.shape[1]):
            signal = dnase[:, i]
            color = colors[i % len(colors)]
            plt.plot(signal, label=selected_organs[i], color=color, marker=".", linestyle="None", alpha=0.7, markersize=2)
        plt.legend(loc="upper right")
        plt.xlabel("bp")
        plt.ylabel("DNASE")
        plt.title("AlphaGenome DNASE")
        plt.grid(True)
        plt.axvline(x=pad_len, color="red", linestyle="--", linewidth=1)
        plt.axvline(x=pad_len + dna_len, color="red", linestyle="--", linewidth=1)
        img_path = f"static/dnase_{os.path.basename(fasta_path)}.png"
        plt.savefig(img_path, dpi=300, bbox_inches="tight")
        plt.close()

    return img_path, "\n".join(logs)
