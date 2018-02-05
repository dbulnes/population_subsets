# Created by: David Bulnes
# 2/4/18
# Copyright 2018, David Bulnes
# Contact: d@vidbuln.es

# Problem statement:
# The 2010 Census puts population_list of 26 largest US metro areas at:
# 18897109, 12828837, 9461105, 6371773, 5965343, 5946800, 5582170, 5564635, 5268860, 4552402, 4335391,
# 4296250, 4224851, 4192887, 3439809, 3279833, 3095313, 2812896, 2783243, 2710489, 2543482, 2356285, 2226009,
# 2149127, 2142508, and 2134411
#
# Can you find a subset of these areas where a total of exactly 100,000,000 people live, assuming the census estimates
# are exactly right? Provide the answer and code or reasoning used.
###################
# Solution and rationale:
# Approaching this problem from a generic standpoint, we really want to find all subsets 's' in a given set 'S',
# of size 'N', whose integer elements sum exactly to our target sum value, 'T'.
#
# This problem is a type of knapsack problem (https://en.wikipedia.org/wiki/Knapsack_problem#Subset-sum_problem) known
# as a Subset-sum problem. There are a number of algorithmic approaches to this type of problem, including those that
# take a Dynamic programming approach and memoize the data. These approaches use recursion, testing sums by
# including and excluding the current element in the given subset. I have decided not to implement this
# approach as it becomes inefficient from a storage and time complexity standpoint because the asymtotic execution
# time is linearly proportional to 'T' and 'N'. In this case, 'T' (100,000,000 people) is proportionally much larger
# than the size of our data we iterate over, 'N' (26 population_list/cities), yielding a runtime complexity of O(T*N)

# When summing population subsets (or any positive integer subset), we care about combinations not permutations,
# as addition is commutative. For a set S of size N, there exists 2^N combinatoric subsets of S, which can be
# proven using induction and some simple test cases with N = 2 or 3. Given there are 2^N possible population subsets,
# we must sum these 2^N subsets to look for our . Thus we arrive at an approximate runtime of = O(2^N), thus removing
#  the targetSum population, 'T', from influencing runtime complexity.

# It is notable that the problem statement asks to find a single subset that sums to our total, rather than
# all possible subsets that match this criteria. This means we exit as soon as we find the first matching subset.
# This program could be easily modified to append all matching population subset tuples to a returned list.
# It can be similarly modified to return the first N numbers of matching population subsets. Logically, returning
# all matching population subsets leads to the longest execution time.

# The combinations() function from itertools provides a very convenient generator that yields all combinations of
# a given size, from a given list.

# Answer:
# There indeed exists a single subset of the given population list whose elements sum to 100,000,000:
# [18897109, 12828837, 9461105, 6371773, 5946800, 5582170, 5268860, 4552402, 4335391, 4296250, 4224851,
# 3279833, 3095313, 2812896, 2543482, 2226009, 2142508, 2134411]
#
from itertools import combinations
import time

# Let's declare our population and target sum here, for ease of access and editing.
populations = [18897109, 12828837, 9461105, 6371773, 5965343, 5946800, 5582170, 5564635, 5268860, 4552402,
                       4335391, 4296250, 4224851, 4192887, 3439809, 3279833, 3095313, 2812896, 2783243, 2710489,
                       2543482, 2356285, 2226009, 2149127, 2142508, 2134411]

target = 100000000


def find_matching_subset(population_list, target_sum):
    """
    Return a subset of population_list whose elements sum to target_sum, if such a subset exists

    Args:
        population_list: list of population_list (positive integers)
        target_sum: the sum (positive integer) of population_list we are looking for, using subsets of population_list
    """
    # Find the total sum of all population_list and check for some base cases
    total_population_sum = sum(population_list)
    # If the target population sum is equal to the summation of the full population set, return population_list
    # Also return if we have an empty population set (a sum of 0)
    if total_population_sum == target_sum or total_population_sum == 0:
        return population_list

    # If we cannot reach the target population sum with the summation of the full population_list set, we already know
    # that no solution exists
    if total_population_sum < target_sum:
        return []

    # After covering the base cases, we start by making sure the list is sorted in descending order
    population_list.sort(key=int, reverse=True)

    # We now iterate through all depth levels of possible subsets, up to the size of our population set
    for subset_depth in range(len(population_list)):
        # As the original population set is sorted in descending order, we know that
        # sum(population_list[0:subset_depth]) represents the maximum sum possible for that depth.
        # If the maximum sum at a given depth is less than our target_sum, we can skip that depth entirely.
        # This optimization leads to an approximate 3-4x improvement in execution time. This improvement
        # is proportional to the magnitude difference between our individual populations and the target_sum,
        # and thus is potentially zero for arguments where the magnitude difference is small.
        if sum(population_list[0:subset_depth]) < target_sum:
            continue  # skip this depth
        for population_subset in combinations(population_list, subset_depth):
            if sum(population_subset) == target_sum:
                return population_subset  # return our matching subset

    return []  # return an empty list if we've exhausted our search empty-handed


if __name__ == "__main__":
    start_time = time.time()  # record our start time
    result = find_matching_subset(populations, target)
    end_time = (time.time() - start_time)  # record our end time

    if result:
        print "Found population subset that sums to %s in %s seconds:" % (target, end_time)
        print result
    else:
        print "Failed to find a matching population subset in %s seconds" % end_time
