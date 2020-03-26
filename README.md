# Coronavirus Testing
This python script brings an idea of testing multiple subjects with small amount of Covid-19 test kits as possible.
There are several assumptions to acknowledge:
- Testing kits are valuable and should be use wisely.
- Taking samples from subjects is much cheaper. Hence, many Samples can be taken from a single individual.
- It is possible to connect several samples in order to check all of them together with a single test kit. 
  If at least one of the samples is positive - the whole test kit will result a positive answer.


## Algorithm example:

Having these assumptions, we will want to use binary numbers to connect samples in various ways in order to pin point the positive subjects.
For example, lets take 7 subjects in our testing. 
We will give each one of them a binary number between 1 to 7 (this list of numbers will be called 'sample_id'):  
1 - 001  
2 - 010  
3 - 011  
4 - 100  
5 - 101  
6 - 110  
7 - 111  

In this case there will be 3 test kits. In each kit we will puts the sample of every subject that has '1' in the the related position.
For an instant, the first kit will have all the samples of subjects that has '1' in the *first* position:   
1 - 00**1**     
3 - 01**1**  
5 - 10**1**  
7 - 11**1**  

The second kit will have all the subjects with '1' in the *second* position:    
2 - 0**1**0  
3 - 0**1**1  
6 - 1**1**0  
7 - 1**1**1  

And so on..


## Finding potential positive subjects:

Now lets say there is one sick subject which his number is '010'. When we will check all three kits, only the second will return positive.
If we will look on the result of the kits as a binary number, we will get '010' (only the second kit is positive - '1')
The only subject that has his sample only in the second position is subject number '2' aka '010' (otherwise other digits were '1' as well and not '0') 

Lets say also subject 6 (110) is positive. Now, the result we will get include test kit 2 (the second) and kit 3 (the third).
The number of the result will be '110'. 
In this case there are more then one options for positive subjects (they will be called 'potential_positive'):  
2 - 010  
4 - 100  
6 - 110  

Notice that these numbers chained with bitwise OR between them will result the same as ower test result - '110'

In order to find the exact positive subjects will have to use more test kits (at most 3 if we dont know how many are positive), but we certainly narrow the number of subjects down.
This kind of testing is most efficient when the number of actual positive is relativly low to the number of total subjects.
For an instant, in case of 255 subjects with only 1 positive subject (~0.5%) the algorithm should be highly effective at narrowing the potential_positive subjects.
This algorithm is best used on a population that is not at high risk of being positive.


## Using more kits - sample_ids:

In order to get more narrow group of potential_positive subbjects it is possible to add more kits.
That results in more ways to give more then one number to every subject (more 'sample_id's).
In this case we can pin a smaller group with the cost of more test kit. 
But it also helps to overcome the problem when the positive subject\s have their samples in many kits, meaning they have numbers with many '1's.
Back to ower example, if subject 7 is positive the kits will result with the number '111' that can have many different combinations of positive subjects (like '110' and '001' etc.)
This cases results in very large gruops of potential_positives and the effectiveness of the algorithm is severely damaged.
More sample ids can cover such cases. 
For example giving more numbers (by adding 3 more kits) in a descending way rather then ascending or just give them randomly.
Subject 7 can have the sample id '111' but also '001' whith is much better for the algorithm in case he is positive.

The script will have to recognize each subject and its corresponding sample ids using the subjects_dict.


## Operating the script:

In order to run the algorithm without using the classes methods, 
it is possible to use the functions in test_run.py only by changing the constant values or entering parameters to the desired function.
`NUM_OF_SUBJECTS_IN_TEST` - Best used with binary numbers like '0b1111', '0b1111111' but can also accept decimal numbers like '37'  
`NUM_OF_TEST_CASES` - For running multiple test cases with the same parameters and getting its statistics.  
`SICK_PERCENTAGE` - The percentage of positive subjects out of the goupe of all subjects.  
`TYPES_OF_SAMPLE_IDS` - list of different ways of giving sample ids to each subject.   
The number of kits that will be added to the test case depends on the number of subjects that need to get this id.
There are 3 different ways of numbering:  
`CoronaTestStat.ASC` = 0  
`CoronaTestStat.DEC` = 1  
`CoronaTestStat.RANDOM` = 2    
Example for a list:  
```TYPES_OF_SAMPLE_IDS =[CoronaTestStat.RANDOM, CoronaTestStat.DEC, CoronaTestStat.RANDOM, CoronaTestStat.RANDOM]```

For more complicated applications, just look at the documentations, it ain't rocket science:)