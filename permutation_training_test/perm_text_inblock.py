import numpy as np
import os
import sys

seed = int(sys.argv[1])
print(f"permutation in-block with seed {seed}")

with open('files_root/alldata-id_p3gram.txt', encoding='utf8') as f:
    dataset = f.readlines()

np.random.seed(seed)
n = len(dataset)
b = n // 8
seq = np.arange(n)
for i in range(4):
    seq[i*b: i*b + b] = np.random.permutation(b) + i * b
with open('alldata-id_p3gram.txt', 'w', encoding='utf8') as f:
    for i, ind in enumerate(seq):
        f.write(f"_*{i}{dataset[ind][dataset[ind].find(' '):]}")

with open('permutation_training_test/seq.txt', 'w') as f:
    for ind in seq[:n//2]:
        f.write(str(ind))
        f.write(' ')

