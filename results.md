---
layout: base
title:  Results
---


PCA(relation linéaires) umap(relation non lihnéaire) graphique accuracy (graphic pour chaque split), tableau de résultat (descr metrics comment les intèrbpéter) matrice de confusion (ce que ça veut dire) feature importance (tableau utilisation) strip chart
All graphs can be saved and will be saved by default in SVG format. This can be changed in the ResultAgregatedTab.py file at the beginning of the file.

## Data

### Principal Component Analysis (PCA)

The PCA extracts the dimensions with the bigger variance to highlight the clusters in the data. 
For more information see this [a wikipedia article](https://en.wikipedia.org/wiki/Principal_component_analysis).

The slider under the figure allows the visualization of the PCA computed on a certain number of 
feature (indicated on the slider). The 'used' indicator refers to the number of features used by the model to
give a prediction. The 'all' indicator refers to the PCA computed on all the data.
The PCA detects linear relationships in the data.

### Uniform Manifold Approximation and Projection for Dimension Reduction (UMAP)

The UMAP is a dimensionality reduction technique to highlights the non-linear relationships in the data. For more detail
see the [a official page](https://umap-learn.readthedocs.io/en/latest/). The UMAP can be used in the same way
as the tSNE but is generally considered better. One of the difference is the random initialisation for the tSNE
as opposed to the Graph Laplacian for the UMAP. Another problem of tSNE is the use of the Kullback-Leibler (KL) divergence
which makes it impossible to preserve global distances, see more [a here](https://towardsdatascience.com/why-umap-is-superior-over-tsne-faa039c28e99).






