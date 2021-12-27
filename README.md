
# Download and prepare the datasets
## Document embedding on IMDB review dataset
Run

    python download.py

to download needed files from [Thongtan's project](https://github.com/tanthongtan/dv-cosine)

Run 

    python IMDB_splits/collect_and_download.py
    python IMDB_splits/gather_all.py

to download and process the splits of the IMDB datset used in [previous work](https://github.com/allenai/dont-stop-pretraining)s.

# Re-evaluation of Document Vectors using Cosine Similarity
This part includes experiments in the 3rd section of the thesis.
## Restoring the correct order (3.3 in the thesis)

In the work of DV-ngrams-cosine, a preprocessed dataset instead of the original IMDB review dataset was used. The preprocessed dataset consists of three files, for unigrams (1gram), unigrams + bigrams, unigrams + bigrams + trigrams (3gram), respectively. Noticeably, 1gram and 3gram have different orders of documents. In the ensemble, DV-ngrams-cosine vectors were trained with 3gram, while BON vectors were extracted from 1gram, thus the mismatching problem. We restored the correct order by solving this sorting problem with counting sort: argsort(3gram, order=1gram).

First, documents from both 1gram and 3gram were processed so that each document from 1gram should be exactly the same as the corresponding document from 3gram. Then the proposed sorting problem was solved by counting sort with a hash table. The retrieved order was then checked to reassure that it was a real permutation of the original order (no repeats).

## Evaluate the ensemble (3.4 in the thesis)

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

## Restoring the preprocessing method (3.3 in the thesis)

To ensure the preprocessed files (1gram and 3gram) were indeed from the original IMDB review dataset, and to enable further works of ours that can directly compare with the original work, the preprocessing method for 1gram was restored. A preprocessing method was proposed and then tested, by directly comparing the documents in 1gram and the preprocessed documents from the original IMDB review dataset with the proposed preprocessing method.

Run

    python original_to_1gram.py

to reproduce the experiments in this part. It will output "matched" if everything went well, otherwise it will throw an assertion error. Check the function "normalize_text" in original_to_1gram.py for details of this preprocessing method.

## Permutation before training (3.5 in the thesis)

Whether or not to shuffle the dataset before embedding training might make a difference in the quality of the trained embeddings. So a couple of tests were run shuffling the dataset in-block or cross-block before training. Here only the code for shuffling and restoring the order of document vectors after training is provided, because it is difficult to streamline test with the original training script.

Run `permutation_training_test/perm_text_inblock.py` or `permutation_training_test/perm_text.py` to shuffle the 3gram file in-block or cross-block and store a shuffled copy in the main dir, ready to be used by the original training script in the folder src.

After the training of each test, run `permutation_training_test/restore_order.py` to restore the order of the trained vectors in the main dir.

Our test showed that the original training script is free of this shuffling/not-shuffling problem. Refer to the 3.5 of the thesis for detailed test results.

## Document Vectors using Cosine Simialrity + BON: gridsearch

run 

    python ensemble_gs.py
    


## Document Vectors using Cosine Similarity + RoBERTa: gridsearch

run 

    python roberta/roberta.py

to finetune the RoBERTa model and extract embeddings for the documents.



# Sub-sampling training tests
This part includes experiments in the 4th section in the thesis.

run

    python imdb_runs_experiments.py

to run all experiments. **The requires a working java installation**.

Use `imdb_runs_experiments_report.ipynb` to check out all the results and plots.

# Dimensionality reduction
This part includes experiments in the 5th section in the thesis.

All the experiments and results are collected in `dr_test.ipynb`.

