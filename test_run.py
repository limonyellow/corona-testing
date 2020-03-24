from utils.binary import all_bins_matches_or

from classes.corona_testing import CoronaTesting
from classes.corona_test_stat import CoronaTestStat


NUM_OF_SUBJECTS_IN_TEST = 0b1111111
NUM_OF_TEST_CASES = 100

def run_corona_test_fixed():
    # Creating the test object and initialize the subject's names.
    test = CoronaTesting(NUM_OF_SUBJECTS_IN_TEST)
    test.generate_subjects_by_num()
    # Adding multiple test ids to each subject.
    test.add_num_sample_id()
    test.add_num_sample_id(reverse=True)
    test.add_random_sample_id()
    # Create the dictionary with all the test ids of each subject.
    test.generate_subjects_dict()

    # Generates sick subject randomly.
    test.generate_infected(2)
    test.infected_subjects = ['subject#42', 'subject#126']
    # Calculates the result of the testing on all subjects,
    # having the generated infected subjects among them to make some of the test positive.
    test.generate_test_result()
    test.find_potential_positive()

    test.find_groups_that_match_result()

    # Show the statistics of the test.
    test.show_full_stats()
    test.show_limit_stats()

def run_corona_test():
    # Creating the test object and initialize the subject's names.
    test = CoronaTesting(NUM_OF_SUBJECTS_IN_TEST)
    test.generate_subjects_by_num()
    # Adding multiple test ids to each subject.
    test.add_num_sample_id()
    test.add_num_sample_id(reverse=True)
    test.add_random_sample_id()
    # Create the dictionary with all the test ids of each subject.
    test.generate_subjects_dict()

    # Generates sick subject randomly.
    test.generate_infected(2)
    # test.infected_subjects = ['subject#11']
    # Calculates the result of the testing on all subjects,
    # having the generated infected subjects among them to make some of the test positive.
    test.generate_test_result()
    test.find_potential_positive()

    # Show the statistics of the test.
    test.show_full_stats()
    test.show_limit_stats()

def run_test_stat():
    regular_test_stat = CoronaTestStat(num_of_subjects=NUM_OF_SUBJECTS_IN_TEST,
                                       num_of_test_cases=NUM_OF_TEST_CASES,
                                       infection_percentage=5,
                                       test_id_types=[CoronaTestStat.RANDOM, CoronaTestStat.RANDOM, CoronaTestStat.RANDOM, CoronaTestStat.RANDOM])
    regular_test_stat.run_all_test_cases()
    regular_test_stat.show_statistics()

if __name__ == '__main__':

    run_corona_test_fixed()
    # run_test_stat()


