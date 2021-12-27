import json
import subprocess
import os

def save_config(nDim, nb:bool, lr, imdb_data_path, suffix='', **kargs):
    nb_string = 'nb' if nb else 'full'
    config = {
        'filename': imdb_data_path,
        'nDim': nDim,
        'nb': nb,
        'n': 500,
        'minTf': 0,
        'lr': lr,
        'nEpoch': 40,
        'subSamp': nb,
        'nbA': 2,
        'nbB': 3,
        'vecPath': f'imdb_runs_results/imdb_vectors_{nb_string}_{lr:.0e}{suffix}.jsonl',
        'logPath': f'imdb_runs_results/imdb_log_{nb_string}_{lr:.0e}{suffix}.txt',
        'test': True,
        'Cs': [0.01, 0.1, 1, 10, 20, 100, 1000, 10000],
        'verbose': 0
    }
    config.update(kargs)
    with open('config.json', 'w') as f:
        json.dump(config, f)
    return


if __name__=="__main__":
    imdb_data_path = "files_root/imdb_data.jsonl"
    results_dir = "imdb_runs_results"
    max_ind = 0
    with open(imdb_data_path) as f:
        for line in f:
            item = json.loads(line)
            max_ind = max(max_ind, max(item["elementIds"]))
    nDim = max_ind + 1
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)
    subprocess.run(['javac', '-cp', 'dvscript;build/jars/gson-2.8.9.jar', '-d', 'build/classes', 'dvscript/dv/cosine/java/Run.java'])

    nb_list = [False, True]
    lr_list = [1e-2, 1e-3, 1e-4, 1e-5]
    for nb in nb_list:
        for lr in lr_list:
            print(f"nb: {nb}, lr: {lr}")
            save_config(nDim, nb, lr, imdb_data_path)
            subprocess.run(['java', '-cp', 'build/classes;build/jars/gson-2.8.9.jar', 'dv.cosine.java.Run'])

    nb_list = [False, True]
    lr_list = [1e-4]
    for nb in nb_list:
        for lr in lr_list:
            print(f"nb: {nb}, lr: {lr}, nepoch: 120")
            save_config(nDim, nb, lr, imdb_data_path, suffix="_120epoch", nEpoch=120)
            subprocess.run(['java', '-cp', 'build/classes;build/jars/gson-2.8.9.jar', 'dv.cosine.java.Run'])

    

    
    