#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def bayes_risk_discrete(discrete_A, discrete_B, W, q):
    """
    R = bayes_risk_discrete(discrete_A, discrete_B, W, q)

    Compute bayesian risk for a discrete strategy q

    :param discrete_A['Prob']:      pXk(x|A) given as a (n, ) np.array
    :param discrete_A['Prior']:     prior probability pK(A)
    :param discrete_B['Prob']:      pXk(x|B) given as a (n, ) np.array
    :param discrete_B['Prior']:     prior probability pK(B)
    :param W:                       cost function np.array (states, decisions)
                                    (nr. of states and decisions is fixed to 2)
    :param q:                       strategy - (n, ) np.array, values 0 or 1
    :return:                        bayesian risk - python float
    """
    probA = discrete_A['Prob']
    probB = discrete_B['Prob']

    priorA = discrete_A['Prior']
    priorB = discrete_B['Prior']
    
    len_prob = np.size(probB)
    p_xA = probA * priorA
    p_xC = probB * priorB


    R = np.sum(p_xA * W[0,q] + p_xC * W[1,q])
    return R


def find_strategy_discrete(discrete_A, discrete_B, W):
    """
    q = find_strategy_discrete(distribution1, distribution2, W)

    Find bayesian strategy for 2 discrete distributions.

    :param discrete_A['Prob']:      pXk(x|A) given as a (n, ) np.array
    :param discrete_A['Prior']:     prior probability pK(A)
    :param discrete_B['Prob']:      pXk(x|B) given as a (n, ) np.array
    :param discrete_B['Prior']:     prior probability pK(B)
    :param W:                       cost function np.array (states, decisions)
                                    (nr. of states and decisions is fixed to 2)
    :return:                        q - optimal strategy (n, ) np.array, values 0 or 1
    """
    probA = discrete_A['Prob']
    probB = discrete_B['Prob']

    priorA = discrete_A['Prior']
    priorB = discrete_B['Prior']


    # distribution1['Prior'] = 0.3
    # distribution2['Prior'] = 0.7
    # distribution1['Prob'] = np.array([0.2, 0.3, 0.4, 0.1])
    # distribution2['Prob'] = np.array([0.5, 0.4, 0.1, 0.0])

    p_xA = probA * priorA
    p_xC = probB * priorB 

    R_xA = np.zeros(np.size(p_xA), dtype=float)
    R_xB = np.zeros(np.size(p_xA), dtype=float)
    for i in range(np.size(p_xA)):
        R_xA[i] = p_xA[i] * W[0,0] + p_xC[i] * W[1,0]
        R_xB[i] = p_xA[i] * W[0,1] + p_xC[i] * W[1,1]
    
    q = np.zeros(np.size(p_xA), dtype=int)
    for i in range(np.size(p_xA)):
        if R_xA[i] <= R_xB[i]:
            q[i] = 0
        else:
            q[i] = 1
    return q


def classify_discrete(measurements, q):
    """
    function label = classify_discrete(measurements, q)

    Classify discrete measurement using a strategy q.

    :param measurements:    test set discrete measurements, (n, ) np.array, values from <-10, 10>
    :param q:               strategy (21, ) np.array of 0 or 1
    :return:                image labels, (n, ) np.array of 0 or 1
    """
    label = q[np.array(measurements + 10, dtype=np.int32)]

    return label


def classification_error(predictions, labels):
    """
    error = classification_error(predictions, labels)

    :param predictions: (n, ) np.array of values 0 or 1 - predicted labels
    :param labels:      (n, ) np.array of values 0 or 1 - ground truth labels
    :return:            error - classification error ~ a fraction of predictions being incorrect
                        python float in range <0, 1>
    """
    
    error = np.sum(predictions != labels) / np.size(labels)
    return error


def find_strategy_2normal(distribution_A, distribution_B):
    """
    q = find_strategy_2normal(distribution_A, distribution_B)

    Find optimal bayesian strategy for 2 normal distributions and zero-one loss function.

    :param distribution_A:  parameters of the normal dist.
                            distribution_A['Mean'], distribution_A['Sigma'], distribution_A['Prior'] - python floats
    :param distribution_B:  the same as distribution_A

    :return q:              strategy dict
                               q['t1'], q['t2'] - decision thresholds - python floats
                               q['decision'] - (3, ) np.int32 np.array decisions for intervals (-inf, t1>, (t1, t2>, (t2, inf)
                               If there is only one threshold, q['t1'] should be equal to q['t2'] and the middle decision should be 0
                               If there is no threshold, q['t1'] and q['t2'] should be -/+ infinity and all the decision values should be the same
                                (0 preferred if both strategies would have the same risk)
    """
    m_A = distribution_A['Mean']
    s_A = distribution_A['Sigma']
    p_A = distribution_A['Prior']
    m_B = distribution_B['Mean']
    s_B = distribution_B['Sigma']
    p_B = distribution_B['Prior']


    a = s_A**2 - s_B**2
    b = 2 * ( (s_B**2) * m_A - (s_A**2) * m_B )
    l = np.log( (s_A / s_B ) * (p_B / p_A))
    c = (s_A**2) * (m_B**2) - (s_B**2) * (m_A**2) - 2*(s_A**2) * (s_B**2) * l
    q = {
        't1': None,
        't2': None,
        'decision': np.zeros(3, dtype=np.int32)
    }

    # extreme priors
    eps = 1e-10
    if p_A < eps:
        q['decision'] = np.array([1,1,1])
        q['t1'] = np.inf
        q['t2'] = -np.inf
    elif p_B < eps:
        q['decision'] = np.array([0,0,0])
        q['t1'] = -np.inf
        q['t2'] = np.inf
    else:
        pass
        if a == 0:
            # same sigmas -> not quadratic
            if b == 0:
                # same sigmas and same means -> not even linear
                if c >= 0: 
                    q['decision'] = np.array([0,0,0])
                    q['t1'] = -np.inf
                    q['t2'] = np.inf
                else:
                    q['decision'] = np.array([1,1,1])
                    q['t1'] = np.inf
                    q['t2'] = -np.inf
            else:
                # same sigmas, different means -> linear equation
                if b > 0:
                    q['decision'] = np.array([1,0,0])
                    q['t1'] = -b / (2 * a)
                    q['t2'] = np.inf
                else:
                    q['decision'] = np.array([0,0,1])
                    q['t1'] = -np.inf
                    q['t2'] = -b / (2 * a)
                
        else:
            # quadratic equation
            D = b**2 - 4 * a * c
            if D > 0:
                t1 = (-b - np.sqrt(D)) / (2 * a)
                t2 = (-b + np.sqrt(D)) / (2 * a)
                if a > 0:
                    q['t1'] = t1
                    q['t2'] = t2
                    q['decision'] = np.array([0,1,0])
                else:
                    q['t1'] = t2
                    q['t2'] = t1
                    q['decision'] = np.array([1,0,1])
            elif D == 0:
                t = -b / (2 * a)
                if a > 0:
                    q['t1'] = t
                    q['t2'] = t
                    q['decision'] = np.array([0,1,0])
                else:
                    q['t1'] = t
                    q['t2'] = t
                    q['decision'] = np.array([1,0,1])
            elif D < 0:
                if a > 0:
                    q['decision'] = np.array([0,0,0])
                    q['t1'] = -np.inf
                    q['t2'] = np.inf
                else:
                    q['decision'] = np.array([1,1,1])
                    q['t1'] = np.inf
                    q['t2'] = -np.inf

    return q


def bayes_risk_2normal(distribution_A, distribution_B, q):
    """
    R = bayes_risk_2normal(distribution_A, distribution_B, q)

    Compute bayesian risk of a strategy q for 2 normal distributions and zero-one loss function.

    :param distribution_A:  parameters of the normal dist.
                            distribution_A['Mean'], distribution_A['Sigma'], distribution_A['Prior'] python floats
    :param distribution_B:  the same as distribution_A
    :param q:               strategy
                               q['t1'], q['t2'] - float decision thresholds (python floats)
                               q['decision'] - (3, ) np.int32 np.array 0/1 decisions for intervals (-inf, t1>, (t1, t2>, (t2, inf)
    :return:    R - bayesian risk, python float
    """
    m_A = distribution_A['Mean']
    s_A = distribution_A['Sigma']
    p_A = distribution_A['Prior']
    m_B = distribution_B['Mean']
    s_B = distribution_B['Sigma']
    p_B = distribution_B['Prior']

    Fa_t1 = norm.cdf(q['t1'], m_A, s_A)
    Fa_t2 = norm.cdf(q['t2'], m_A, s_A)
    Fb_t1 = norm.cdf(q['t1'], m_B, s_B)
    Fb_t2 = norm.cdf(q['t2'], m_B, s_B)

    first = 0
    second = 0
    third = 0
    if q['decision'][0] == 0:
        first = p_A * Fa_t1
    elif q['decision'][0] == 1:
        first = p_B * Fb_t1

    if q['decision'][1] == 0:
        second = p_A * (Fa_t2 - Fa_t1)
    elif q['decision'][1] == 1:
        second = p_B * (Fb_t2 - Fb_t1)  
    if q['decision'][2] == 0:
        third = p_A * (1 - Fa_t2)
    elif q['decision'][2] == 1:
        third = p_B * (1 - Fb_t2)   

    R = 1 - (first + second + third)
    return R


def classify_2normal(measurements, q):
    """
    label = classify_2normal(measurements, q)

    Classify images using continuous measurements and strategy q.

    :param imgs:    test set measurements, np.array (n, )
    :param q:       strategy
                    q['t1'] q['t2'] - float decision thresholds
                    q['decision'] - (3, ) int32 np.array decisions for intervals (-inf, t1>, (t1, t2>, (t2, inf)
    :return:        label - classification labels, (n, ) int32
    """
    label = q['decision'][np.digitize(measurements, [q['t1'], q['t2']])]
    return label

################################################################################
#####                                                                      #####
#####             Below this line are already prepared methods             #####
#####                                                                      #####
################################################################################


def compute_measurement_lr_cont(imgs):
    """
    x = compute_measurement_lr_cont(imgs)

    Compute measurement on images, subtract sum of right half from sum of
    left half.

    :param imgs:    set of images, (h, w, n)
    :return:        measurements, (n, )
    """
    assert len(imgs.shape) == 3

    width = imgs.shape[1]
    sum_rows = np.sum(imgs, dtype=np.float64, axis=0)

    x = np.sum(sum_rows[0:int(width / 2), :], axis=0) - np.sum(sum_rows[int(width / 2):, :], axis=0)

    assert x.shape == (imgs.shape[2], )
    return x


def visualize_discrete(discrete_A, discrete_B, q):
    """
    visualize_discrete(discrete_A, discrete_B, q)

    Visualize a strategy for 2 discrete distributions.

    :param discrete_A['Prob']:      pXk(x|A) given as a (n, ) np.array
    :param discrete_A['Prior']:     prior probability pK(A)
    :param discrete_B['Prob']:      pXk(x|B) given as a (n, ) np.array
    :param discrete_B['Prior']:     prior probability pK(B)
    :param q:                       strategy - (n, ) np.array, values 0 or 1
    """

    joint_A = discrete_A['Prob'] * discrete_A['Prior']
    joint_B = discrete_B['Prob'] * discrete_B['Prior']

    max_prob = np.max([joint_A, joint_B])

    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    plt.title("Joint probabilities and strategy q")
    plt.xlabel("feature")
    plt.ylabel("joint probabilities")

    bins = np.array(range(joint_A.size + 1)) - int(joint_A.size / 2)

    width = 0.75
    bar_plot_A = plt.bar(bins[:-1], joint_A, width=width, color='b', alpha=0.75)
    bar_plot_B = plt.bar(bins[:-1], joint_B, width=width, color='r', alpha=0.75)

    plt.legend((bar_plot_A, bar_plot_B), (r'$p_{XK}(x,A)$ / decision A', r'$p_{XK}(x,C)$ / decision C'))

    sub_level = - max_prob / 8
    height = np.abs(sub_level) * 0.9
    for idx in range(len(bins[:-1])):
        b = bins[idx]
        col = 'r' if q[idx] == 1 else 'b'
        patch = patches.Rectangle([b - 0.5, sub_level], 1, height, angle=0.0, color=col, alpha=0.75)
        ax.add_patch(patch)

    plt.ylim(bottom=sub_level)
    plt.text(bins[0], -max_prob / 12, 'strategy q', color='w')
    ax.axhline(y=0, color='k', linewidth=0.8)

    # Put labels in the middle of bins (-10 ... 10)
    bin_centers = np.arange(-10, 11, 1)
    ax.set_xticks(bin_centers)
    ax.set_xticklabels([str(v) for v in bin_centers])

    # Mark bin transitions with minor ticks (-10.5 ... 10.5)
    bin_edges = np.arange(-10.5, 10.5 + 1e-9, 1.0)
    ax.set_xticks(bin_edges, minor=True)

    # Style: visible transition ticks, hidden major tick marks (keep labels)
    ax.tick_params(axis='x', which='major', length=0)
    ax.tick_params(axis='x', which='minor', length=4)

    ax.set_xlim(bin_edges[0], bin_edges[-1])
    # plt.show();


def visualize_2norm(cont_A, cont_B, q):
    n_sigmas = 5
    n_points = 200

    A_range = (cont_A['Mean'] - n_sigmas * cont_A['Sigma'],
               cont_A['Mean'] + n_sigmas * cont_A['Sigma'])
    B_range = (cont_B['Mean'] - n_sigmas * cont_B['Sigma'],
               cont_B['Mean'] + n_sigmas * cont_B['Sigma'])
    start = min(A_range[0], B_range[0])
    stop = max(A_range[1], B_range[1])

    xs = np.linspace(start, stop, n_points)
    A_joint = cont_A['Prior'] * norm.pdf(xs, cont_A['Mean'], cont_A['Sigma'])
    B_joint = cont_B['Prior'] * norm.pdf(xs, cont_B['Mean'], cont_B['Sigma'])

    fig = plt.figure(figsize=(6, 3))
    colors = ['r', 'b']
    plt.axhline(y=0, color='k', linewidth=0.8)
    plt.plot(xs, A_joint, c=colors[0], label='A')
    plt.plot(xs, B_joint, c=colors[1], label='C')

    plt.axvline(x=q['t1'], c='k', lw=0.5, ls=':')
    plt.axvline(x=q['t2'], c='k', lw=0.5, ls=':')


    offset = 0.000007
    sub_level = -0.000025
    left = xs[0]
    right = xs[-1]

    def clip(x, lb, ub):
        res = x
        if res < lb:
            res = lb
        if res > ub:
            res = ub
        return res
    t1 = clip(q['t1'], xs[0], xs[-1])
    t2 = clip(q['t2'], xs[0], xs[-1])

    patch = patches.Rectangle([left, sub_level], t1-left, -sub_level-offset, angle=0.0,
                              color=colors[q['decision'][0]], alpha=0.75)
    plt.gca().add_patch(patch)
    patch = patches.Rectangle([t1, sub_level], t2-t1, -sub_level-offset, angle=0.0,
                              color=colors[q['decision'][1]], alpha=0.75)
    plt.gca().add_patch(patch)
    patch = patches.Rectangle([t2, sub_level], right-t2, -sub_level-offset, angle=0.0,
                              color=colors[q['decision'][2]], alpha=0.75)
    plt.gca().add_patch(patch)
    plt.legend()

    plt.title("Joint probabilities and strategy q")
    plt.xlabel("image LR feature")
    plt.ylabel("joint probabilities")
    plt.xlim(start, stop)


def compute_measurement_lr_discrete(imgs):
    """
    x = compute_measurement_lr_discrete(imgs)

    Calculates difference between left and right half of image(s).

    :param imgs:    set of images, (h, w, n) (or for color images (h, w, 3, n)) np.array
    :return:        (n, ) np.array of values in range <-10, 10>,
    """
    assert len(imgs.shape) in (3, 4)
    assert (imgs.shape[2] == 3 or len(imgs.shape) == 3)

    mu = -563.9
    sigma = 2001.6

    if len(imgs.shape) == 3:
        imgs = np.expand_dims(imgs, axis=2)

    imgs = imgs.astype(np.int32)
    height, width, channels, count = imgs.shape

    x_raw = np.sum(np.sum(np.sum(imgs[:, 0:int(width / 2), :, :], axis=0), axis=0), axis=0) - \
            np.sum(np.sum(np.sum(imgs[:, int(width / 2):, :, :], axis=0), axis=0), axis=0)
    x_raw = np.squeeze(x_raw)

    x = np.atleast_1d(np.round((x_raw - mu) / (2 * sigma) * 10))
    x[x > 10] = 10
    x[x < -10] = -10

    assert x.shape == (imgs.shape[-1], )
    return x


def montage(images, colormap='gray'):
    """
    Show images in grid.

    :param images:  np.array (h, w, n)
    """
    h, w, count = np.shape(images)
    h_sq = int(np.ceil(np.sqrt(count)))
    w_sq = h_sq
    im_matrix = np.ones((h_sq * h, w_sq * w)) * 255

    image_id = 0
    for k in range(w_sq):
        for j in range(h_sq):
            if image_id >= count:
                break
            slice_w = j * h
            slice_h = k * w
            im_matrix[slice_h:slice_h + w, slice_w:slice_w + h] = images[:, :, image_id]
            image_id += 1
    # plt.imshow(im_matrix, cmap=colormap)
    # plt.axis('off')
    return im_matrix


################################################################################
#####                                                                      #####
#####             Below this line you may insert debugging code            #####
#####                                                                      #####
################################################################################

def main():
    # HERE IT IS POSSIBLE TO ADD YOUR TESTING OR DEBUGGING CODE
    print(np.array([0]*10 + [1] + [0]*10))
    pass

if __name__ == "__main__":
    main()
