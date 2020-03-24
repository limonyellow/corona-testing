from typing import List


def get_intersection_between_lists(lists: List[List]) -> List:
    """
    Creates a list which contains only the elements that appear in all of the given lists.
    @param lists: List of lists.
    @return: List with the intersection elements.
    """
    intersection_list = lists.pop()
    for ls in lists:
        intersection_list = list(set(intersection_list) & set(ls))
    return intersection_list
