import requests
import os 
from pathlib import Path 
import pickle

# dictionary with urls to datasets 
urls = dict()
urls['powerDemand']=['http://www.cs.ucr.edu/~eamonn/discords/power_data.txt']

for urlKey in urls:
    rootDir = Path('datasets', urlKey, 'raw')
    rootDir.mkdir(parents=True, exist_ok=True)
    for url in urls[urlKey]:
        print('download started', url)
        filename = rootDir.joinpath(Path(url).name)
        response = requests.get(url)
        print('saving to', filename.with_suffix('.txt'))
        filename.write_bytes(response.content)


    # more general approach if multiple datasets are stored as text files
    for filepath in rootDir.glob('*.txt'):
        with open(str(filepath)) as f:
            labeled_data=[]
            for i, line in enumerate(f):
                tokens = [float(token) for token in line.split()]
                tokens.append(1.0) if 8254 < i < 8998 or 11348 < i < 12143 or 33883 < i < 34601 else tokens.append(0.0)
                labeled_data.append(tokens)

            # labeled dataset stored as a file .pkl file
            labeled_whole_dir = rootDir.parent.joinpath('labeled', 'whole')
            labeled_whole_dir.mkdir(parents=True, exist_ok=True)
            with open(str(labeled_whole_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
                pickle.dump(labeled_data, pkl)

            # Divide between training and test data
            labeled_train_dir = rootDir.parent.joinpath('labeled','train')
            labeled_train_dir.mkdir(parents=True,exist_ok=True)
            labeled_test_dir = rootDir.parent.joinpath('labeled','test')
            labeled_test_dir.mkdir(parents=True,exist_ok=True)

            with open(str(labeled_train_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
                pickle.dump(labeled_data[15287:33432], pkl)
            with open(str(labeled_test_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
                pickle.dump(labeled_data[501:15287], pkl)