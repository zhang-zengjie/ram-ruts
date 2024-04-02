import control as ctrl
import numpy as np
from numpy.linalg import eig
from scipy.linalg import solve_discrete_lyapunov as dlyap

# Checks whether all elements in list are identical
def check(list):
    return all(i == list[0] for i in list)

def get_coordinates(bounds):
    x_coordinates = [bounds[0], bounds[1], bounds[1], bounds[0]]
    y_coordinates = [bounds[2], bounds[2], bounds[3], bounds[3]]
    return x_coordinates, y_coordinates

def get_center(bounds):
    return (bounds[0] + bounds[1])/2, (bounds[2] + bounds[3])/2


# Probabilistic reachable tube computation
def PRT(sys, Q, R):

    # Compute stabilizing feedback controller
    K, _, _ = ctrl.dlqr(sys.A, sys.B, Q, R)
    A_K = sys.A - sys.B * K
    Eig, _ = eig(A_K)
    assert np.any(abs(Eig) < 1)  # Ensure the feedback controller is stabilizing

    # Probabilistic reachable tube (Spherical)
    SigmaInf = dlyap(A_K, sys.Sigma)
    assert np.sum(abs(SigmaInf)) != 0  # Check for zero matrix
    assert np.sum(SigmaInf - np.diag(np.diagonal(SigmaInf))) == 0  # Check whether matrix is diagonal
    assert check(np.diagonal(SigmaInf))  # Check whether diagonal matrix is spherical

    return SigmaInf[0, 0], K  # Remember the diagonal value and stabilizing feedback gain

def checkout_largest_in_list(lst, m):
    # Enumerate the list to get index-value pairs, then sort by values in descending order
    sorted_indexes = sorted(enumerate(lst), key=lambda x: x[1], reverse=True)
    
    # Extract the first m indexes from the sorted list
    result_indexes = [index for index, _ in sorted_indexes[:m]]
    
    return result_indexes

def checkout_largest_in_dict(dictionary, m):
    sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items[:m])

def calculate_probabilities(spec_list, risk):

        l = len(spec_list)
        spec_prob = np.ones((l, ))

        for i in range(l):
            for j in spec_list[i].ts:
                spec_prob[i] -= risk[j]
        return spec_prob

def calculate_risks(spec_list, risk):

        l = len(spec_list)
        spec_prob = np.zeros((l, ))

        for i in range(l):
            for j in spec_list[i].ts:
                spec_prob[i] += risk[j]
        return spec_prob


def config_logger(logger, filename):
    logger.basicConfig(filename=filename, level=logger.DEBUG, format='%(asctime)s: %(message)s', filemode='w')

    console = logger.StreamHandler()
    console.setLevel(logger.INFO)  # Set the desired logger level for console output

    # Define a formatter for the console handler
    formatter = logger.Formatter('%(asctime)s: %(message)s')
    console.setFormatter(formatter)

    # Add the console handler to the root logger
    logger.getLogger('').addHandler(console)