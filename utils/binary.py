from typing import List, Dict
from itertools import combinations


def dec_to_bin(dec_num: int) -> str:
    """
    Converts a number to its binary form as string.
    @param dec_num: Decimal number.
    @return: Binary number as string.
    """
    return bin(dec_num)[2:]


def bin_len(dec_num: int) -> int:
    """
    Calculates the number of digits in the binary form of a number.
    @param dec_num: Decimal number.
    @return: Length of its binary form.
    """
    return len(dec_to_bin(dec_num))


def all_bins_matches_or(num: int, no_zero: bool = True) -> List[int]:
    """
    Generate all the binary numbers that have the digit '1' in the same position as the given number and nowhere else.
    '0' can appear anywhere. All these numbers can create together the given number by using the 'or' ('|') operation.
    @param num: The number to find matching binary numbers.
    @param no_zero: Set to True if the result shouldn't contain the number '0'.
    @return: List of matching binary numbers.
    """
    bins = []
    bin_range = range(2**len(bin(num)[2:]))[1:] if no_zero else range(2**len(bin(num)[2:]))
    for bin_num in bin_range:
        if num | bin_num == num:
            bins.append(bin_num)
    return bins


def find_groups_that_match(iterable: List[int], match: int, size_of_group: int = None) -> List[List[int]]:
    """
    Creates combinations of numbers in the given size.
    For each combination checks if all of its elements connected by bitwise 'or', equals the number to match.
    If so, adds the combination to the returned list.
    @param iterable: List of numbers.
    @param match: Number to check if the created groups are match with.
    @param size_of_group: The number of numbers in a group.
    @return: List with all the groups that matches the match number.
    """
    if not size_of_group:
        size_of_group = len(iterable)
    or_matches = []
    all_combo = combinations(iterable, size_of_group)
    for combo in all_combo:
        or_res = 0
        for bin_num in combo:
            or_res = or_res | bin_num
        if or_res == match:
            or_matches.append(list(combo))
    return or_matches


def find_all_groups_that_match(iterable: list, match: int, max_group_size: int = None) -> Dict[int, List[List[int]]]:
    """
    Finds all the combinations of numbers in every size from 1 to 'max_group_size',
    that the result of chaining each one of elements of the combination with bitwise 'or', matches the given number.
    @param iterable: List of numbers.
    @param match: Number to check if the created groups are match with.
    @param max_group_size: The maximum number of elements in a group.
    @return: Dictionary with keys as the size of the groups and values as a list of groups with the corresponding size.
    """
    if not max_group_size:
        max_group_size = len(iterable)
    groups_dict = {}
    for size in range(max_group_size + 1)[1:]:
        groups_dict[size] = find_groups_that_match(iterable, match, size)
    return groups_dict


if __name__ == '__main__':
    ls = [64, 42, 126, 110]
    inf = [42, 126]
    match = 126
    size = 5
    x = find_groups_that_match(ls, match, size)
    for i in x:
        print(i)

    print('--------')
    x = combinations(ls, size)
    for i in x:
        print(i)

    dict = find_all_groups_that_match(ls, match)
    print(dict)

