import subprocess
from collections import Counter
from time import clock


ALGOS = ["giftwrap", "grahamscan", "monotonechain"]
ORDERED_ALGOS = ["giftwrap", "grahamscan"]
PREFIXES = ["A_", "B_"]
NUMBERS = ["3000", "6000", "9000", "12000", "15000", "18000", "21000", "24000", "27000", "30000"]
RUN_COUNT = 5  #Number of times to run each test


def readresults():
    resultsA, resultsB, data = [], [], ""
    with open('results.txt') as f:
        data = f.read().splitlines()
        resultsA = data[1:11]
        resultsB = data[13:23]
    return resultsA, resultsB


def runtests():
    resultsA, resultsB = readresults()

    for algo in ALGOS:
        #print("-_"*80)
        for prefix in PREFIXES:
            for number in NUMBERS:
                time_elapsed, i = 0, 0
                while i < RUN_COUNT-1:
                    t = clock()
                    p1 = subprocess.Popen("python convexhull.py "+algo+" "+prefix+number+'.dat', stdout = subprocess.PIPE)
                    temp = str(p1.stdout.readline().strip())
                    time_elapsed += clock() - t
                    temp = temp[2:-1]  #Remove silly cli clutter
                    if prefix == "A_":
                        ans = resultsA[NUMBERS.index(number)].strip()
                    elif prefix == "B_":
                        ans = resultsB[NUMBERS.index(number)].strip()
                    i += 1

                time_elapsed = time_elapsed/RUN_COUNT

                if algo in ORDERED_ALGOS:
                    if temp == ans:
                        result = " Passed "
                    else:
                        print("Expected:", ans)
                        print("Received:", temp)
                        result = " Failed "
                else:
                    if sorted(temp) == sorted(ans):
                        result = " Passed "
                    else:
                        print("Expected:", ans)
                        print("Received:", temp)
                        result = " Failed "

                #print("-_"*80)
                print(algo, result, prefix+number, " Time:", time_elapsed)
                #print("-_"*80)


#  Log output to file with:
#  python tester.py > algoname_analysis.txt
runtests()
