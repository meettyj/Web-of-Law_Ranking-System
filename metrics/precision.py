import numpy as np

def precisionAtK(actual, predicted, k=10):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        # print('in enumeration')
        # print('i: %d,   p: %s'%(i,p))
        # print('predicted[:i]: ', predicted[:i])
        # print('p: ', p)
        # the statement after and can be removed, since it was use to prevent duplication.
        if p in actual and p not in predicted[:i]:
            # print('here we at: ', p)
            num_hits += 1.0
            score += num_hits / (i+1.0)
            # print('score: ', score)

    if not actual:
        print('should not be enter')
        return 0.0

    # return score / min(len(actual), k)
    precision = score / k
    # print('precision at top %d is %f' %(k, precision))
    return precision



def apk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    k_list = [i+1 for i in range(k)]
    # print('k_list: ', k_list)
    return np.mean([precisionAtK(actual,predicted,i) for i in k_list])


def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return np.mean([precisionAtK(a,p,k) for a,p in zip(actual, predicted)])
