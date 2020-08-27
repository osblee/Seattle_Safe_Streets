"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This file will test the confidence interval of a hypothetical
dataset.
"""
import numpy as np
import scipy.stats as stats


def test_confidence_example():
    """
    Tests the confidence interval functionalitiy with a given example found
    to test all confidence intervals typcally.
    """
    spring_size = 105
    fall_size = 108
    confidence = 0.90
    spring_total = 125
    fall_total = 150
    prop_spring = float(spring_size) / spring_total
    prop_fall = float(fall_size) / fall_total
    var = prop_spring * (1 - prop_spring) / spring_total + \
        prop_fall * (1 - prop_fall) / fall_total
    se = np.sqrt(var)
    significance = 1 - confidence
    z = stats.norm(loc=0, scale=1).ppf(confidence + significance / 2)
    prop_diff = prop_spring - prop_fall
    confint = prop_diff + np.array([-1, 1]) * z * se

    print("expected using TI-84 Two Proportion Z test", "0.039", "0.201")
    print("n1=125", "x1=108")
    print("n1=150", "x1=105")
    print(list(confint))


def main():
    test_confidence_example()


if __name__ == "__main__":
    main()
