
# Document embeddings for text classification
This repository contains code for the thesis under the same name.

Code in folder "src" and file "ensemble.py" are from [Thongtan's project](https://github.com/tanthongtan/dv-cosine). 

## Download and prepare the datasets
### Document embedding on IMDB review dataset
Run

    python download.py

to download needed files from [Thongtan's project](https://github.com/tanthongtan/dv-cosine)

Run 

    python IMDB_splits/collect_and_download.py
    python IMDB_splits/gather_all.py

to download and process the splits of the IMDB datset used in [previous work](https://github.com/allenai/dont-stop-pretraining)s.

## Re-evaluation of Document Vectors using Cosine Similarity
This part includes experiments in the 3rd section of the thesis.
### Document matching between 1gram and 3gram (3.2 in the thesis)

In the work of DV-ngrams-cosine, a preprocessed dataset instead of the original IMDB review dataset was used. The preprocessed dataset consists of three files, for unigrams (1gram), unigrams + bigrams, unigrams + bigrams + trigrams (3gram), respectively. Noticeably, 1gram and 3gram have different orders of documents. In the ensemble, DV-ngrams-cosine vectors were trained with 3gram, while BON vectors were extracted from 1gram, thus the mismatching problem. We restored the correct order by solving this sorting problem with counting sort: argsort(3gram, order=1gram).

First, documents from both 1gram and 3gram were processed so that each document from 1gram should be exactly the same as the corresponding document from 3gram. Then the proposed sorting problem was solved by counting sort with a hash table. The retrieved order was then checked to reassure that it was a real permutation of the original order (no repeats).

### Restoring the preprocessing method (3.3 in the thesis)

To ensure the preprocessed files (1gram and 3gram) were indeed from the original IMDB review dataset, and to enable further works of ours that can directly compare with the original work, the preprocessing method for 1gram was restored. A preprocessing method was proposed and then tested, by directly comparing the documents in 1gram and the preprocessed documents from the original IMDB review dataset with the proposed preprocessing method.

Run

    python original_to_1gram.py

to reproduce the experiments in this part. It will output "matched" if everything went well, otherwise it will throw an assertion error. Check the function "normalize_text" in original_to_1gram.py for details of this preprocessing method.

### Evaluate the ensemble (3.4 in the thesis)

The ensemble was evaluated by the original code, with both the original and the correct DV-BON matching. Some additional tests with shuffed matching were also carried out. The shuffing schemes are as shown the following table. Embeddings were repeatedly read and written to new files to enable the tests with the original code `ensemble.py`. All tests involving shuffing were run for 30 times to better estimate the scores.

||in-class|cross-class|
|----------------------------------|:--:|:--:|
|test set                          |A|B|
|train and test sets (respectively)|C|D|

Run

    python test_with_origin.py

to reproduce the experiments for the first 2 parts (restoring the correct order and evaluate the ensemble). Find the log and report in folder "test_logs"

Our results are shown in the following table

||Score Mean|Score Std|
|----------------------------------|:-----:|:-----:|
|original matching| 97.42||
|correct matching| 93.68||
|test set shuffed in-class (A)| 96.58| 0.07|
|test set shuffed cross-class (B)| 61.80| 0.25|
|train/test shuffed in-class (C)| 97.43| 0.08|
|train/test shuffed cross-class (D)| 91.64| 0.08|

Comparing A and B shows that when test set is shuffled dis-respecting the classes, the score dropped very significantly, which means the embedding is important in the ensemble. C reproduced very similar scores as the original matching, implying contribution of data leakage to the high score. D serves as a control group to C.



### Permutation before training (3.5 in the thesis)

Whether or not to shuffle the dataset before embedding training might make a difference in the quality of the trained embeddings. So a couple of tests were run shuffling the dataset in-block or cross-block before training.

Run

    permutation_training_test/before_train_perm_test.py

to do the shuffling and vector training. **The requires a working java installation**

Then refer to permutation_training_test/vectors_comparison.ipynb for tests and results.

Our test showed that the original training script is free of this shuffling/not-shuffling problem. The set of vectors provided by the author of the original work are different than the sets trained by us, but they are similar in effect.

### Document Vectors using Cosine Simialrity + BON: gridsearch (3.6 in the thesis)

run 

    python ensemble_gs.py
    
to run the grid-search, and then refer to dv+bon_results.ipynb for results.

### Document Vectors using Cosine Similarity + RoBERTa: gridsearch (3.7 in the thesis)

run 

    python roberta/roberta.py

to finetune the RoBERTa model and extract embeddings for the documents.

Then check out dv+roberta.ipynb for additional experiments and results.



## Naive Bayesian Sub-sampling and analysis on the training process
This part includes experiments in the 4th section in the thesis.

run

    python imdb_runs_experiments.py

to run all experiments with embedding training. **This requires a working java installation**.

Use `imdb_runs_experiments_report.ipynb` to check out all the results and plots.

Check out dvnb+roberta.ipynb for the ensemble of DV (with sub-sampling) and RoBERTa.

## Dimensionality reduction
This part includes experiments in the 5th section in the thesis.

All the experiments and results are collected in `dr_test.ipynb`. **This requires a working java installation**

