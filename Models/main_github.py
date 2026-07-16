import os
import pickle
import argparse
import warnings

import numpy as np
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD

import BIONIC

warnings.filterwarnings("ignore")

# Set a specific GPU here if needed, e.g.:
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def parse_args():
    parser = argparse.ArgumentParser(description='BIONIC trainer')
    parser.add_argument('--fold', dest='fold', help='Fold to test', default=0, type=int)
    parser.add_argument('--seed', dest='seed', help='Random seed', default=500, type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    print('Fold: ', args.fold)
    print('Seed: ', args.seed)

    database = 'MMIST'
    folds = 10

    # Output directory for saved train/test label arrays
    results_dir = os.path.join('.', 'Results', 'MMIST_weights')
    os.makedirs(results_dir, exist_ok=True)

    aucs = []
    bals = []

    for fold in range(folds):
        folds_file = os.path.join('.', 'MMIST', f'{folds}folds_{database}.p')
        print('Loading test and validation folds.')
        [fold_tst, dict_fold_val] = pickle.load(open(folds_file, 'rb'))

        X1 = np.load('./MMIST_new/view_Clinical_semi.npy')
        X3 = np.load('./MMIST_new/view_Genomic_semi.npy')

        Y = np.load('./MMIST_new/Y_semi.npy')

        pos_tr = fold_tst[fold][0]
        pos_tst = fold_tst[fold][1]

        X1_tr, X1_tst = X1[pos_tr, :], X1[pos_tst, :]
        X3_tr, X3_tst = X3[pos_tr, :], X3[pos_tst, :]

        ##################
        # SVD, fit on the training partition
        # only and then applied to the test partition, per modality.
        ##################
        N_COMPONENTS_CT = 100
        N_COMPONENTS_MRI = 100
        N_COMPONENTS_WSI = 100

        X2_raw = np.load('./MMIST_new/view_CT_semi.npy')
        X4_raw = np.load('./MMIST_new/view_MRI_semi.npy')
        X5_raw = np.load('./MMIST_new/view_WSI_semi.npy')

        X2_raw_tr, X2_raw_tst = X2_raw[pos_tr, :], X2_raw[pos_tst, :]
        X4_raw_tr, X4_raw_tst = X4_raw[pos_tr, :], X4_raw[pos_tst, :]
        X5_raw_tr, X5_raw_tst = X5_raw[pos_tr, :], X5_raw[pos_tst, :]

        svd_ct = TruncatedSVD(n_components=N_COMPONENTS_CT, random_state=args.seed)
        X2_tr = svd_ct.fit_transform(X2_raw_tr)
        X2_tst = svd_ct.transform(X2_raw_tst)

        svd_mri = TruncatedSVD(n_components=N_COMPONENTS_MRI, random_state=args.seed)
        X4_tr = svd_mri.fit_transform(X4_raw_tr)
        X4_tst = svd_mri.transform(X4_raw_tst)

        svd_wsi = TruncatedSVD(n_components=N_COMPONENTS_WSI, random_state=args.seed)
        X5_tr = svd_wsi.fit_transform(X5_raw_tr)
        X5_tst = svd_wsi.transform(X5_raw_tst)
        ##################

        Y = Y[:, np.newaxis]
        Y_tr = Y[pos_tr, :]
        Y_tst = Y[pos_tst, :]

        X1 = np.vstack((X1_tr, X1_tst))
        X2 = np.vstack((X2_tr, X2_tst))
        X3 = np.vstack((X3_tr, X3_tst))
        X4 = np.vstack((X4_tr, X4_tst))
        X5 = np.vstack((X5_tr, X5_tst))

        myModel = BIONIC.BIONIC(Kc=100, Kp=1, prune=1, SS_sep=1, Yy=Y_tst, seed_init=args.seed)
        X0_t = myModel.struct_data(X1, 'reg', 1)
        X1_t = myModel.struct_data(X2, 'reg', 1)
        X2_t = myModel.struct_data(X3, 'reg', 1)
        X3_t = myModel.struct_data(X4, 'reg', 1)
        X4_t = myModel.struct_data(X5, 'reg', 1)
        Y1_tr = myModel.struct_data(Y_tr, 'mult', 0)
        Y1_tst = myModel.struct_data(Y_tst, 'mult', 0)

        myModel.fit(X0_t, X1_t, X2_t, X3_t, X4_t, Y1_tr, max_iter=200,
                    Y_tst=Y1_tst, AUC=0, ACC=0, verbose=1)

        Y_pred = myModel.compute_predictions(X_tst=[None], m_in=[0, 1, 2, 3, 4], m_out=5)
        Y_pred_tr = myModel.compute_predictions(X_tst=[None], m_in=[0, 1, 2, 3, 4], m_out=5, tr=1)

        auc_tst = metrics.roc_auc_score(Y_tst, Y_pred)
        aucs.append(auc_tst)

        fpr_tr, tpr_tr, thresholds_roc = metrics.roc_curve(Y_tr, Y_pred_tr)
        optimal_idx_tr = np.argmax(tpr_tr - fpr_tr)
        optimal_threshold_tr = thresholds_roc[optimal_idx_tr]
        print('Optimal threshold train: ', optimal_threshold_tr)

        predicted_classes_tr = (Y_pred >= optimal_threshold_tr).astype(int)
        balanced_accuracy_tr = metrics.balanced_accuracy_score(Y_tst, predicted_classes_tr)
        bals.append(balanced_accuracy_tr)

        print('Train results: ')
        print(f"Optimal Threshold: {optimal_threshold_tr}")
        print(f"AUC: {auc_tst}")
        print(f"Balanced Accuracy: {balanced_accuracy_tr}")

        np.save(os.path.join(results_dir, 'Y_MMIST_tr.npy'), Y_tr)
        np.save(os.path.join(results_dir, 'Y_MMIST_tst.npy'), Y_tst)

    print('Mean AUC: ', np.mean(aucs), ' +- ', np.std(aucs))
    print('Mean Balanced Accuracy: ', np.mean(bals), ' +- ', np.std(bals))


if __name__ == '__main__':
    main()
