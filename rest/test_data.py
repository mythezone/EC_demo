import numpy as np 
import random, time ,sys, os, json

def generate_result(num,max_t=1000,record=100,population=5):
    results=[]
    candidates=[i for i in range(record)]
    for _ in range(num):
        test_data={
                    "time":random.random()*10,
                    "iteration":random.randint(1,max_t),
                    "fitness":random.randint(50,99),
                    "individual": [random.choice(candidates) for _ in range(population)],
                    "finger":[random.randint(0,2**450) for _ in range(population)]
                }

        results.append(test_data)
    return results


def overall_result(results):
    ttc=0
    popu=0
    best=-1
    best_index=-1
    for i in range(len(results)):
        result=results[i]
        ttc+=result['time']
        popu+=len(result['indiviual'])
        if result['fitness']>best:
            best=result['fitness']
            best_index=i

    res={"ttc":ttc,
          "popu":popu,
          "best":best,
          "bestsolution":best_index
    }
    return res

if __name__ == '__main__':
    a=generate_result(3)
    print(a)
