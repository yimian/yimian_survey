# SIF_ZH

This is the implement of a sentence embedding algorithm in [the paper](https://openreview.net/forum?id=SyK00v5xx) "A Simple but Tough-to-Beat Baseline for Sentence Embeddings" in Python3 and in Chinese corpus.


## Install

```angular2html
$ pip install -r requirements.txt
```

## Get started
To get started, you need:
- A corpus to train word2vec model and get frequency of word.
- A corpus of sentences (here is some question about tea in Chinese).

Then:
- Config the path of data in `process_data.py` .
- run the `process_data.py` to get a `dict` from word to frequency.
- run the `main.py` to get a similarity task test.

## Source code description
- `process_data.py` provides the function to build the `dict` from word to frequency for a corpus.
- `params.py` provides a Class `Params` to pack the parameters in to a object
- `sif_embedding.py` provides the function to get the weighted embedding, SIF embedding for sentences and a demo of the similarity task.



