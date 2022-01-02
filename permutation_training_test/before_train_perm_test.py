import subprocess
import os
import shutil


if __name__=="__main__":
    if not os.path.isdir("permutation_training_test/vectors"):
        os.mkdir("permutation_training_test/vectors")
        
    subprocess.run(['javac', '-cp', 'src', '-d', 'build/classes_src', 'src/dv/cosine/java/NeuralNetwork.java'])

    seeds = [12, 22, 32]
    # in-block perm
    for i, seed in enumerate(seeds):
        subprocess.run(["python", "permutation_training_test/perm_text_inblock.py", str(seed)])
        subprocess.run(['java', '-cp', 'build/classes_src', 'dv.cosine.java.NeuralNetwork'])
        subprocess.run(["python", "permutation_training_test/restore_order.py"])
        shutil.move(f"train_vectors_r.txt", "permutation_training_test/vectors/train_vectors_ib{i}.txt")
        shutil.move(f"test_vectors_r.txt", "permutation_training_test/vectors/test_vectors_ib{i}.txt")

    # cross-block perm
    for i, seed in enumerate(seeds):
        subprocess.run(["python", "permutation_training_test/perm_text.py", str(seed)])
        subprocess.run(['java', '-cp', 'build/classes_src', 'dv.cosine.java.NeuralNetwork'])
        subprocess.run(["python", "permutation_training_test/restore_order.py"])
        shutil.move(f"train_vectors_r.txt", "permutation_training_test/vectors/train_vectors_cb{i}.txt")
        shutil.move(f"test_vectors_r.txt", "permutation_training_test/vectors/test_vectors_cb{i}.txt")
    
    os.remove("alldata-id_p3gram.txt")
    os.remove("train_vectors.txt")
    os.remove("test_vectors.txt")
    print("done")

