import os

os.chdir('permutation_training_test')
vectors = []
with open('../train_vectors.txt') as f:
    vectors.extend(f.readlines())

with open('../test_vectors.txt')  as f:
    vectors.extend(f.readlines())

with open('seq.txt') as f:
    seq = map(int, f.read().split())

reverse_seq = [0] * len(vectors)
for i, ind in enumerate(seq):
    reverse_seq[ind] = i

with open('../train_vectors_r.txt', 'w') as f:
    for i in range(25000):
        f.write(vectors[reverse_seq[i]])

with open('../test_vectors_r.txt', 'w') as f:
    for i in range(25000, 50000):
        f.write(vectors[reverse_seq[i]])

