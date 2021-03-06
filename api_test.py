from sklearn.externals import joblib
from preprocessing.dataset import read_dataset
from training.cross_validation import evaluate
from training.query import query
import numpy as np
import time


def pretrain():
    # with open('pretrained/results.csv', 'w+') as results_file:
    #     results_file.write('mmr,train_size,test_size,roc_auc\n')

    for i in range(31):
        if i < 20:
            offset = 200
        elif i < 25:
            offset = 250
        else:
            offset = 300

        mmr_low = 2000 + 100 * i - offset
        mmr_base = 2000 + 100 * i
        mmr_high = 2000 + 100 * i + offset

        train_features, _ = read_dataset('706e_train_dataset.csv', low_mmr=mmr_low, high_mmr=mmr_high)
        test_features, _ = read_dataset('706e_test_dataset.csv', low_mmr=mmr_low, high_mmr=mmr_high)

        (train_size, test_size, roc_auc) = evaluate(train_features,
                                                    test_features,
                                                    cv=0,
                                                    save_model='pretrained/' + str(mmr_base) + '.pkl')

        with open('pretrained/results.csv', 'a+') as results_file:
            results_file.write('%s,%d,%d,%.3f\n' % (str(mmr_base), train_size, test_size, roc_auc))


def main():

    synergies = np.loadtxt('pretrained/synergies_all.csv')
    counters = np.loadtxt('pretrained/counters_all.csv')
    similarities = np.loadtxt('pretrained/similarities_all.csv')

    start_time = time.time()
    query(3011, [59, 56, 54, 48, 34], [40, 41, 52, 68], synergies, counters, similarities)
    end_time = time.time()

    print (end_time - start_time) * 1000, 'ms'


if __name__ == '__main__':
    main()
