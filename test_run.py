from utils.binary import bin_len
from classes.corona_testing import CoronaTesting
from classes.corona_test_stat import CoronaTestStat


NUM_OF_SUBJECTS_IN_TEST = 0b1111
NUM_OF_TEST_CASES = 100
SICK_PERCENTAGE = 0.5
TYPES_OF_SAMPLE_IDS = [CoronaTestStat.RANDOM, CoronaTestStat.RANDOM]
# TYPES_OF_SAMPLE_IDS = [CoronaTestStat.ASC, CoronaTestStat.DEC]


def run_corona_test(num_of_subjects_in_test=NUM_OF_SUBJECTS_IN_TEST, infection_percentage=SICK_PERCENTAGE):
    # Creating the test object and initialize the subject's names.
    test = CoronaTesting(num_of_subjects_in_test)
    test.generate_subjects_by_num()
    # Adding multiple test ids to each subject.
    test.add_num_sample_id()
    test.add_opposite_sample_id()
    # test.add_num_sample_id(reverse=True)
    # test.add_random_sample_id()
    # Create the dictionary with all the test ids of each subject.
    test.generate_subjects_dict()

    # Generates sick subject randomly.
    test.generate_infected(infection_percentage)
    # Calculates the result of the testing on all subjects,
    # having the generated infected subjects among them to make some of the test positive.
    test.generate_test_result()
    test.find_potential_positive()

    test.find_groups_that_match_result(max_size_of_group=None)

    # Show the statistics of the test.
    test.show_full_stats()
    test.show_limit_stats()
    print(test.get_num_of_test_kits())
    print(test.get_num_of_samples_taken())


def run_multi_test_stat(num_of_subjects_in_test=NUM_OF_SUBJECTS_IN_TEST,
                        num_of_test_cases=NUM_OF_TEST_CASES,
                        infection_percentage=SICK_PERCENTAGE,
                        sample_id_types=None):
    if not sample_id_types:
        sample_id_types = TYPES_OF_SAMPLE_IDS

    # Creating the test Stat object.
    regular_test_stat = CoronaTestStat(num_of_subjects=num_of_subjects_in_test,
                                       num_of_test_cases=num_of_test_cases,
                                       infection_percentage=infection_percentage,
                                       sample_id_types=sample_id_types)
    # Running all test cases.
    regular_test_stat.run_all_test_cases()

    regular_test_stat.show_statistics()


def run_multi_with_optimize_number_of_kits(max_num_of_sample_ids: int = 6,
                                           num_of_subjects_in_test=NUM_OF_SUBJECTS_IN_TEST,
                                           num_of_test_cases=NUM_OF_TEST_CASES,
                                           infection_percentage=SICK_PERCENTAGE):
    """
    Running multiple test cases and changing the number of random sample ids (adding more test kits to every run)
    The final results will show the optimal number of sample ids / kits
    before adding more kits won't narrow the number of potential positive
    more then just use them to check a single subject.
    """
    kits_in_sample_id = bin_len(NUM_OF_SUBJECTS_IN_TEST)
    kits_to_potentials = []
    all_cases = []

    for num_of_sample_ids in range(max_num_of_sample_ids + 1)[1:]:
        sample_ids = [CoronaTestStat.RANDOM for i in range(num_of_sample_ids)]

        test_stat = CoronaTestStat(num_of_subjects=num_of_subjects_in_test,
                                   num_of_test_cases=num_of_test_cases,
                                   infection_percentage=infection_percentage,
                                   sample_id_types=sample_ids)
        test_stat.run_all_test_cases()
        kits_to_potentials.append((test_stat.num_of_test_kits_in_case, test_stat.avg_potential_positive))
        all_cases.append(test_stat)
        test_stat.show_statistics()

    last_case_potentials = (0, NUM_OF_SUBJECTS_IN_TEST)
    for idx, case in enumerate(kits_to_potentials):
        if case[1] >= last_case_potentials[1] - kits_in_sample_id:
            print(f'Optimize num of kits: {last_case_potentials[0]} '
                  f'with {last_case_potentials[1]} potential positive subjects.')
            print(f'Kits to potential positive stats: {kits_to_potentials}')
            return all_cases
        else:
            last_case_potentials = case

    print(f'Optimize num of kits: {last_case_potentials[0]} '
          f'with {last_case_potentials[1]} potential positive subjects.')
    print(f'Kits to potential positive stats: {kits_to_potentials}')
    return all_cases


if __name__ == '__main__':
    run_corona_test()
    # run_multi_test_stat()
    # run_multi_with_optimize_number_of_kits()
