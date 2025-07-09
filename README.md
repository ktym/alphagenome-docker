# AlphaGenome Docker Environment

This Docker image provides a minimal Python environment with [AlphaGenome](https://github.com/google-deepmind/alphagenome?tab=readme-ov-file) and common data science libraries installed. It is designed to replicate a similar environment to Google Colab for offline or local development.

## Included Libraries

- alphagenome
- matplotlib
- pandas
- numpy

## Requirements

- Docker installed (https://docs.docker.com/get-docker/)

## Build the Image

To build the Docker image:

```bash
docker build -t alphagenome-env .
```

This will create an image named `alphagenome-env`.

## Run an Interactive Python Session

To start an interactive Python session inside the container:

```bash
docker run -it --rm alphagenome-env
```

## Use Your AlphaGenome API Key

To run `run.py` with your API key, you can pass it as an environment variable:

```bash
docker run -it --rm \
  -v $(pwd):/alphagenome \
  -e API_KEY=your_real_api_key_here \
  alphagenome-env python run.py
```

Alternatively, create a .env file in this directory with the following content:

```
API_KEY=your_real_api_key_here
```

Then run the container using:

```bash
docker run -it --rm \
  -v $(pwd):/alphagenome \
  --env-file .env \
  alphagenome-env python run.py
```

## Customize Working Directory

By default, the working directory inside the container is set to `/alphagenome`.

You can mount your local project directory to it using:

```bash
docker run -it --rm -v $(pwd):/alphagenome alphagenome-env
```

## Supported analyses types in AlphaGenome

| Output Type         | Description                                                                 | Data / Interpretation                                                |
|---------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------|
| ATAC                | Identifies regions of open chromatin using Tn5 transposase                  | Open chromatin; regulatory accessibility                             |
| CAGE                | Captures transcription start sites (TSS) via 5' capped RNAs                 | Promoter activity; precise TSS location                              |
| DNASE               | Maps DNase I hypersensitive sites                                           | Regulatory elements like enhancers and promoters                     |
| RNA_SEQ             | Measures gene expression via RNA sequencing                                 | Transcript abundance; splicing patterns                              |
| CHIP_HISTONE        | ChIP-seq for histone modifications                                          | Epigenetic marks (e.g., H3K27ac, H3K4me3) indicating active regions   |
| CHIP_TF             | ChIP-seq for transcription factors                                          | TF binding sites; regulatory network inference                       |
| SPLICE_SITES        | Annotated or predicted splice donor/acceptor sites                          | Exon-intron boundaries; splicing signals                             |
| SPLICE_SITE_USAGE   | Quantitative usage level of splice sites                                    | Splicing dynamics; isoform switching                                 |
| SPLICE_JUNCTIONS    | Inferred exon junctions from RNA-seq reads                                  | Alternative splicing patterns                                        |
| CONTACT_MAPS        | Chromatin interaction data (e.g., Hi-C, Micro-C)                            | 3D genome organization; enhancer-promoter loops                      |
| PROCAP              | High-resolution identification of transcription start sites via run-on cap | Active transcription initiation; enhancer activity                   |

## Optional: Use JupyterLab

To run JupyterLab instead of a Python shell, modify the CMD in the Dockerfile or override it:

```bash
docker run -it --rm -p 8888:8888 alphagenome-env jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

Then access it at http://localhost:8888 in your browser.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

