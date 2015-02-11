__author__ = 'faebser'

status = dict()
tests = list()


def add_test(test_reference):
    """
    Add a test to the list to run it later

    :param test_reference: object
    :return None:
    """
    tests.append(test_reference)
    return


def run_all_tests():
    """
    Runs all test and returns a list containing tuples with the results
    :return list:
    """
    test_results = list()
    for test in tests:
        test_results.append(test())
    return test_results