import numpy as np

def task():
    sums, products = set(), set()
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            sums.add(i1 + i2)
            products.add(i1 * i2)
    sums, products = sorted(sums), sorted(products)

    sum_lookup = {s: sums.index(s) for s in sums}
    product_lookup = {p: products.index(p) for p in products}

    counts = np.zeros((len(sums), len(products)))
    
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            counts[sum_lookup[i1 + i2], product_lookup[i1 * i2]] += 1

    probabilities = counts / 36

    entropy_AB = -np.sum(probabilities * np.log2(probabilities, where=np.abs(probabilities) > 0.0001))

    probabilities_A = np.sum(probabilities, axis=1)
    entropy_A = -np.sum(probabilities_A * np.log2(probabilities_A, where=np.abs(probabilities_A) > 0.0001))

    probabilities_B = np.sum(probabilities, axis=0)
    entropy_B = -np.sum(probabilities_B * np.log2(probabilities_B, where=np.abs(probabilities_B) > 0.0001))

    entropy_A_B = entropy_AB - entropy_A

    information_AB = entropy_B - entropy_A_B

    return [round(el, 2) for el in [entropy_AB, entropy_A, entropy_B, entropy_A_B, information_AB]]

# Пример:
information_metrics = task()
print("Joint Entropy (H(AB)): ", information_metrics[0])
print("Entropy of A (H(A)): ", information_metrics[1])
print("Entropy of B (H(B)): ", information_metrics[2])
print("Conditional Entropy (H_A(B)): ", information_metrics[3])
print("Mutual Information (I(A,B)): ", information_metrics[4])
