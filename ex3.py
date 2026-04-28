import csv
import math
from collections import Counter
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, recall_score, accuracy_score, precision_score
from sklearn.model_selection import train_test_split

# Distance Functions
def euclidean(p1, p2): return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))
def manhattan(p1, p2): return sum(abs(a-b) for a, b in zip(p1, p2))
def chebyshev(p1, p2): return max(abs(a-b) for a, b in zip(p1, p2))

def get_distance_function(choice):
    return {1: euclidean, 2: manhattan, 3: chebyshev}.get(choice, euclidean)

def compute_k(n_train):
    k = int(0.1 * n_train)
    k = k + 1 if k % 2 == 0 else max(1, k)
    return k

def knn_predict_with_scores(X_train, Y_train, X_test, k, dist_func, weighted=False, all_labels=None):
    distances = []
    for i in range(len(X_train)):
        d = dist_func(X_train[i], X_test)
        distances.append((d, Y_train[i]))

    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]

    scores = {label: 0.0 for label in all_labels} if all_labels is not None else {}

    if weighted:
        for d, label in k_nearest:
            w = 9999 if d == 0 else 1 / (d ** 2)
            scores[label] = scores.get(label, 0) + w
    else:
        for _, label in k_nearest:
            scores[label] = scores.get(label, 0) + 1

    winner = max(scores, key=scores.get)
    return winner, scores

def load_csv(filename, attr_indices):
    X, Y = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None) # Skip header
        for row in reader:
            try:
                X.append([float(row[i]) for i in attr_indices])
                Y.append(row[-1])
            except: continue
    return np.array(X), np.array(Y)

def file_knn():
    filename = r"C:\Users\Administrator\Downloads\archive\Iris.csv"
    indices = list(map(int, input("Indices (e.g. 0 1 2 3): ").split()))
    X, Y = load_csv(filename, indices)
    all_unique_labels = np.unique(Y)

    split = int(input("% Training: ")) / 100
    X_tr, X_te, Y_tr, Y_te = train_test_split(X, Y, train_size=split, random_state=42)

    print(f"\n--- Data Split Information ---")
    print(f"Total training records: {len(X_tr)}")
    print(f"Total testing records:  {len(X_te)}")

    k = compute_k(len(X_tr))
    print(f"Computed K Value: {k}")

    dist_f = get_distance_function(int(input("\nDist (1:Euc, 2:Man, 3:Cheb): ")))
    wt = (int(input("Type (1:Wt, 2:Unwt): ")) == 1)

    preds = [knn_predict_with_scores(X_tr, Y_tr, x, k, dist_f, wt, all_unique_labels)[0] for x in X_te]

    print("\n--- Evaluation Results ---")
    print(f"Accuracy:  {accuracy_score(Y_te, preds):.4f}")
    print(f"Precision: {precision_score(Y_te, preds, average='weighted'):.4f}")
    print(f"Recall:    {recall_score(Y_te, preds, average='weighted'):.4f}")
    print(f"F1-Score:  {f1_score(Y_te, preds, average='weighted'):.4f}")
    print("\nConfusion Matrix:\n", confusion_matrix(Y_te, preds))

def inputKNN():
    n = int(input("Attributes count: "))
    m = int(input("Observations count: "))
    X, Y = [], []
    for i in range(m):
        X.append(list(map(float, input(f"Obs {i+1} attrs: ").split())))
        Y.append(input(f"Obs {i+1} label: "))

    all_unique_labels = np.unique(Y)
    test_pt = list(map(float, input("Test point: ").split()))
    k = int(input("Enter K value: "))
    dist_f = get_distance_function(int(input("Dist (1:Euc, 2:Man, 3:Cheb): ")))
    wt = (int(input("Type (1:Wt, 2:Unwt): ")) == 1)

    # Calculate distances and store with original data for ranking
    all_data = []
    for i in range(m):
        d = dist_f(X[i], test_pt)
        w = 9999 if d == 0 else 1/(d**2)
        all_data.append({'attrs': X[i], 'label': Y[i], 'dist': d, 'weight': w})

    # Sort by distance to determine Rank
    all_data.sort(key=lambda x: x['dist'])
    for index, item in enumerate(all_data):
        item['rank'] = index + 1

    # Distance Table with Rank
    print("\n" + "="*90 + "\n                                  DISTANCE TABLE\n" + "-"*90)
    print(f"{'Rank':<6} | {'Attributes':<25} | {'Label':<12} | {'Distance':<12} | {'Weight':<10}")
    print("-" * 90)
    for item in all_data:
        print(f"{item['rank']:<6} | {str(item['attrs']):<25} | {item['label']:<12} | {item['dist']:<12.4f} | {item['weight']:<10.4f}")
    print("="*90)

    res, scores = knn_predict_with_scores(np.array(X), np.array(Y), test_pt, k, dist_f, wt, all_unique_labels)

    print("\n" + "="*45 + "\n          VOTES / WEIGHT SUMMARY\n" + "-"*45)
    header = "Total Weight" if wt else "Votes (Count)"
    print(f"{'Class Label':<25} | {header:<15}")
    print("-" * 45)
    for label, score in scores.items():
        print(f"{label:<25} | {score:<15.4f}")
    print("="*45)
    print(f"\nFinal Predicted Label: {res}")

if __name__ == "__main__":
    mode = int(input("Select Mode (1: Manual, 2: File): "))
    inputKNN() if mode == 1 else file_knn()
