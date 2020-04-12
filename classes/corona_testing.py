import random
from typing import List, Dict

from utils.lists import get_intersection_between_lists
from utils.binary import all_bins_matches_or, find_all_groups_that_match, opposite_bin


class CoronaTesting:

    COVID19_POSITIVE = 1
    COVID19_NEGATIVE = 0

    def __init__(self, num_of_subjects: int, test_name: str = '', subjects_id: [str] = None,
                 sample_ids: List[List[int]] = None, main_sample_id_num: int = 0):
        self.num_of_subjects = num_of_subjects
        self._num_of_test_kits = len(format(num_of_subjects, 'b'))
        self.test_name = test_name
        # Unique identifier for each subject.
        self.subjects_id = subjects_id if subjects_id else self.generate_subjects_by_num()
        # Unique binary number that represents where the subjects samplings are located.
        # For example, the sample_id '101' suggests the subjects samples located in the first and the third test kits.
        self.sample_ids = sample_ids if sample_ids else []
        # The number of the main sample id that uses for comparison between subjects.
        self.main_sample_id_num = main_sample_id_num
        # Dictionary that holds all the relations between the subject id and its matching sample ids.
        self.subjects_dict = {}
        # The subjects id of the sick subjects. Only generated for simulates test results.
        self.infected_subjects = []
        # The results (binary numbers) that will turn out if some of the test kits in each sample id will be positive.
        self.tests_results = []
        # Sample ids of subjects that are suspected as positive to corona.
        self.potential_positive = []
        # Lists af all numbers of subjects that are suspected as positive.
        # Each List belongs to different sample id (all numbers are normalized to the main sample id numbering.
        self.normalize_potential_positive = []
        # Dictionary that maps group size into possible groups of positive subjects that produce the test results.
        self.potential_positive_in_groups = {}
        # List of subjects that according to the testing are fully confirmed as positive carriers of corona.
        self.confirmed_positive = []

    def show_full_stats(self):
        print(f'Full Corona Testing Stats:')
        print(f'-Subjects_id: {self.subjects_id}')
        print(f'-Subjects_dict: {self.subjects_dict}')
        self._show_stats()

    def show_stats(self):
        print(f'Corona Testing Stats:')
        self._show_stats()

    def _show_stats(self):
        print(f'-Num_of_subjects: {self.num_of_subjects}')
        self.show_num_of_kits()
        self.show_num_of_samples()
        print(f'-Infected_subjects: {len(self.infected_subjects)}')
        self.show_infected()
        print(f'-Tests_results:')
        self.show_test_result()
        print(f'-Number of potential_positive: {len(self.potential_positive)}')
        print(f'-Potential_positive: {[f"{num}--{bin(num)}" for num in self.potential_positive ]}')
        print(f'-Potential positive in groups: {self.potential_positive_in_groups}')

    def show_limit_stats(self):
        print(f'Corona Testing Stats:')
        print(f'-Num_of_subjects: {self.num_of_subjects}')
        print(f'-Infected_subjects: {len(self.infected_subjects)}')
        print(f'-Number of potential_positive: {len(self.potential_positive)}')
        print(f'-Potential_positive: {[f"{num}--{bin(num)}" for num in self.potential_positive ]}')
        print(f'-Potential positive in groups: {self.potential_positive_in_groups}')

    def show_num_of_kits(self):
        print(f'-Number of test kits used: {self.get_num_of_test_kits()}')

    def show_num_of_samples(self):
        print(f'-Number of samples taken from all subjects: {self.get_num_of_samples_taken()}')

    def get_num_of_digits_in_num_of_subjects(self):
        """
        Calculates the number of digits in the binary number of subjects.
        @return: The length of the num of subjects in binary.
        """
        return len(format(self.num_of_subjects, 'b'))

    def get_num_of_test_kits(self) -> int:
        """
        Calculates the number of test kits that will be used in the test by finding the number of binary digits that are
        used in every sample id.
        @return: The number of binary digits in the number of subjects times the number of sample ids taken.
        """
        return self.get_num_of_digits_in_num_of_subjects() * len(self.sample_ids)

    def get_num_of_samples_taken(self):
        """
        Calculates the number of samples that should be taken from all subjects.
        Each '1' in all of the sample ids of a subject represents a sample that should be inserted into the matched
        test kit.
        @return: The total number of samples taken from all subjects.
        """
        samples_counter = 0
        for sample_id in self.sample_ids:
            for num in sample_id:
                samples_counter += format(num, 'b').count('1')
        return samples_counter

    def generate_subjects_by_num(self, default_name: str = 'subject') -> List[str]:
        """
        Creates the unique string id for each subject out of a default name and ascending numbers.
        @param default_name: The string that will attach to every subject id.
        @return: List of subject ids.
        """
        # Todo Check the size? What happens when the size is not 2**x?
        self.subjects_id = [f'{default_name}#{num + 1}' for num in range(self.num_of_subjects)]
        return self.subjects_id

    def add_num_sample_id(self, reverse: bool = False):
        """
        Adds new numbering method to the sample ids. Each subject will receive different number.
        @param reverse: If set to True, the numbering will start from the last subject back to the first.
        """
        test_range = reversed(range(self.num_of_subjects)) if reverse else range(self.num_of_subjects)
        self.sample_ids.append([(num + 1) for num in test_range])

    def add_opposite_sample_id(self, num_of_digits = None):
        """
        Adds new numbering that takes the last sample id list of numbers and change every digit to its opposite.
        Every '1' turns to '0' and '0' into '1'.
        """
        if not num_of_digits:
            num_of_digits = self.get_num_of_digits_in_num_of_subjects()
        sample_id = self.sample_ids[-1]
        opposite_sample_id = []
        for sample in sample_id:
            opposite_sample_id.append(opposite_bin(sample, num_of_digits))
        self.sample_ids.append(opposite_sample_id)

    def add_random_sample_id(self):
        """
        Adds new numbering method to the sample ids. Each subject will receive a different random number.
        """
        sample_id = [num + 1 for num in range(self.num_of_subjects)]
        random_sample_id = []
        for i in range(self.num_of_subjects):
            num = random.choice(sample_id)
            random_sample_id.append(num)
            sample_id.remove(num)
        self.sample_ids.append(random_sample_id)

    def generate_subjects_dict(self):
        """
        Creates the dictionary that maps each subject id as key and its corresponding sample ids.
        """
        subject_sample_ids = [[] for _ in range(len(self.subjects_id))]
        # Grouping all sample ids of the same subject in the same list.
        for sample_id in self.sample_ids:
            for idx, num in enumerate(sample_id):
                subject_sample_ids[idx].append(num)
        # Matching each subject id with his own sample id list.
        self.subjects_dict = {self.subjects_id[i]: subject_sample_ids[i] for i in range(len(self.subjects_id))}

    def generate_infected(self, percentage: float = 1) -> List:
        """
        Generates random sick subjects out of the subjects list according to the requested percentage.
        *In different executions with the same input, the number of sick subject can be different.
        @param percentage: The probability of every subject to be sick.
        @return: The subject ids of the sick chosen subjects.
        """
        for subject in self.subjects_id:
            random_res = random.choices([self.COVID19_POSITIVE, self.COVID19_NEGATIVE], [percentage, 100 - percentage])
            if random_res.pop() == self.COVID19_POSITIVE:
                self.infected_subjects.append(subject)
        return self.infected_subjects

    def create_fixed_infected(self, percentage: float = 1) -> List:
        """
        Generates random sick subjects out of the subjects list.
        The number of sick subjects will be exactly the requested percentage out of the number of subjects.
        *In different executions with the same input, the number of sick subject will stay fixed.
        @param percentage: The percentage of subjects that will be chose as sick.
        @return: The subject ids of the sick chosen subjects.
        """
        num_of_infected = int(self.num_of_subjects * percentage / 100)
        self.infected_subjects = random.sample(self.subjects_id, num_of_infected)
        return self.infected_subjects

    def show_infected(self):
        for idx, infected in enumerate(self.infected_subjects):
            infected_sample_id = [f'{sample_id}--{bin(sample_id)}' for sample_id in self.subjects_dict[infected]]
            print(f'Infected#{idx} - {infected} sample ids: {infected_sample_id}')

    def generate_test_result(self, infected: List = None) -> List[int]:
        """
        Creates the test result that reflects the given infected subjects.
        The method creates a different test results for each sample id.
        The test result is created simply by using bitwise 'or' between each of the sample ids of the sick subjects.
        @param infected: List of sick subjects that their sample ids are found in the subjects dict.
        @return: A list of all the test results in the same order as the sample_ids list.
        """
        if not infected:
            infected = self.infected_subjects
        result_per_test = [0 for i in range(len(self.sample_ids))]
        for infected_subject in infected:
            sample_ids = self.subjects_dict.get(infected_subject)
            for idx, sample_id in enumerate(sample_ids):
                result_per_test[idx] = result_per_test[idx] | sample_id
        self.tests_results = result_per_test
        return self.tests_results

    def show_test_result(self):
        for idx, res in enumerate(self.tests_results):
            print(f'Test_result#{idx} = {res}--{bin(res)}')

    def find_potential_positive(self) -> List[int]:
        """
        Todo Check if works when the subject_id are not full - example - for the case there are only 7 subjects in test
        Find all the subjects that their sample ids matches the equivalent test result.
        This being made be finding all the binary number (=sample ids)
        that can create the binary result with bitwise 'or' between them.
        @return: List of the potential subjects to be sick according to the test results.
        """
        all_potential_positive = [all_bins_matches_or(result) for result in self.tests_results]
        # Normalize all numbers in each different sample id to one main sample id.
        # This being made in order to compare between subjects that came up in different sample ids.
        self.normalize_potential_positive = self._normalize_potential_positive(all_potential_positive,
                                                                               self.main_sample_id_num)

        # After each subject has only a single sample id to recognize it,
        # only the subjects that appear in every list (each list from different sample id), are potentially sick.
        self.potential_positive = get_intersection_between_lists(self.normalize_potential_positive)
        return self.potential_positive

    def _normalize_potential_positive(self, all_potential_positive: List[List[int]],
                                      main_pos: int = 0) -> List[List[int]]:
        """
        Converts every sample id to the main equivalent sample id in the subjects dict.
        @param all_potential_positive: Lists of numbers.
        @param main_pos: The main sample id column in the subjects dict that all numbers will be normalized according to.
        @return: Lists with the potential subjects numbers in the converted form.
        """
        potential_positive_normalized = [[] for i in range(len(all_potential_positive))]
        for key in self.subjects_dict.keys():
            for idx_sample_id, row in enumerate(all_potential_positive):
                if self.subjects_dict[key][idx_sample_id] in row:
                    potential_positive_normalized[idx_sample_id].append(self.subjects_dict[key][main_pos])
        return potential_positive_normalized

    def find_groups_that_match_result(self, max_size_of_group: int = None,
                                      potential_positive: list = None,
                                      match_result: int = None) -> Dict[int, List[List[int]]]:
        """
        Having the potential positive numbers, creating groups of numbers that together connected with bitwise 'or'
        matching the test result.
        This means that every group can be the group of sick subjects that brings to the generated test result.
        @param max_size_of_group: The maximum number of subjects each group can contain.
         Effective when the number of sick subjects is known.
         Otherwise, sets the max size to biggest possible (the number of potentials subjects).
        @param potential_positive: The sample ids numbers of the potential positive subjects.
        @param match_result: The result that the created groups should be matched with.
        @return: Dictionary with keys as the size of the groups
        and values as a list of groups with the corresponding size.
        """
        if not potential_positive:
            potential_positive = self.potential_positive
        if not match_result:
            match_result = self.tests_results[self.main_sample_id_num]
        if not max_size_of_group:
            max_size_of_group = len(potential_positive)

        self.potential_positive_in_groups = find_all_groups_that_match(potential_positive, match_result,
                                                                       max_size_of_group)
        return self.potential_positive_in_groups
