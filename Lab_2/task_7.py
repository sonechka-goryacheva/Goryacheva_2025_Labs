import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


import task_1 as field      
import task_2 as gen_random   
import task_3 as unique     
import task_5 as print_result
import task_6 as cm_timer

with open("data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

@print_result.print_result
def f1(data):
    job_names = list(field.field(data, "job-name"))
    unique_jobs = unique.Unique(job_names, ignore_case=True)
    return sorted(unique_jobs, key=lambda s: s.lower())


@print_result.print_result
def f2(data):
    return list(filter(lambda s: "программист" in s.lower(), data))


@print_result.print_result
def f3(data):
    return list(map(lambda s: f"{s} с опытом Python", data))


@print_result.print_result
def f4(data):
    salaries = list(gen_random.gen_random(len(data), 100000, 200000))
    result = []
    for job, salary in zip(data, salaries):
        result.append(f"{job}, зарплата {salary} руб.")
    return result


if __name__ == "__main__":
    with cm_timer.cm_timer_1():
        f4(f3(f2(f1(data))))