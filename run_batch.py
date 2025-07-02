import sys
import time
import subprocess
import os
import socket
import re

dev_name = None

def main():
    global dev_name
    dev_name = socket.gethostname()
    print(dev_name)
    
    with open(sys.argv[1], "r") as f:
        contents = f.read()
        f.close()
    
    tests = contents.split("\n")

    if (tests[len(tests) - 1] == ""):
        tests = tests[:-1]

    for test in tests:
        setup_experiment(test)
        
def setup_experiment(exp):
    
    
    num_parallel = 10
    
    args = exp.split(" ")
    
    workload = args[5]
    
    
    exp_str = ""
    
    recorded_time = ""
    
    base = ""
    
    base += "taskset -c 0-9,11-29,31-39 perf stat -M  "
    base += args[6]

    base += " /home/mcallisl/gem5/build/ALL/gem5.opt /home/mcallisl/perf_automation/gem5_config.py"
    
    base += " --isa " + args[0]
    base += " --cpu " + args[1]
    base += " --mem " + args[2]
    base += " --cache " + args[3]
    base += " --cores " + args[4]
    base += " --workload " + args[5]
    
    for i in range(0, num_parallel):
        
        s = base
    
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
        
        if (i == 0):
            recorded_time = timestr

        time.sleep(2) # make sure experiments don't have same timestamp
    
        s += " &> "
        d = "/home/mcallisl/perf_automation/output_files/"
        for tmp in args:
            d += tmp + "-"

        d = d[:-1]
        s += d + "/" + timestr + "-" + dev_name

        s += " & "
        
        exp_str += s
        
        if not os.path.exists(d):
            os.makedirs(d)
            print(os.path.exists(d))
        
    exp_str += "wait"
    
    log_experiment(exp_str, recorded_time, args)
    
    run_experiment(exp_str, d, workload)
    
def run_experiment(exp_str, dir_str, workload_str):
    
    result = subprocess.run(exp_str, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("success")
        print(result.stdout)
        print(result.stderr)
    else:
        print("error executing command")
        log_error("error executing command")
        print(result.stderr)
        exit(1)
    
    time.sleep(300)
    
    cleanup = subprocess.run("sudo -S sh -c 'echo 3 > /proc/sys/vm/drop_caches'", shell=True, capture_output=True, text=True, input="hfsdfgjghfe")

    if cleanup.returncode == 0:
        print("success")
        print(cleanup.stdout)
    else:
        print("error executing cleanup")
        log_error("error executing cleanup")
        print(cleanup.stderr)
        exit(1)
        
    extract_data(dir_str, workload_str)
        
    
def extract_data(dir_str, workload_str):
    
    metrics,keys = process_directory(dir_str)
    
    output_str = "/home/mcallisl/perf_automation/extracted_csvs/" + workload_str + "/" + dir_str + ".csv"
    
    write_to_csv(metrics, keys, output_str)
    

def process_directory(directory):
    all_metrics = {}
    all_keys = set()

    for filename in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            metrics = extract_metrics_from_file(full_path)
            all_metrics[filename] = metrics
            all_keys.update(metrics.keys())

    return all_metrics, sorted(all_keys)
    
    
def extract_metrics_from_file(filepath):
    
    metrics = {}
    metric_pattern = re.compile(r'#\s+([\d\.]+)\s+%\s+(\S+)')
    time_elapsed_pattern = re.compile(r'(\d+\.\d+) seconds time elapsed')
    total_uops_pattern = re.compile(r'([\d,]+)\s+UOPS_ISSUED.ANY')

    with open(filepath, 'r') as file:
        for line in file:
            match = metric_pattern.search(line)
            if match:
                percent, metric = match.groups()
                metrics[metric] = percent

            time_match = time_elapsed_pattern.search(line)
            if time_match:
                metrics['time_elapsed'] = time_match.group(1)

            total_match = total_uops_pattern.search(line)
            if total_match:
                metrics['total_uops'] = total_match.group(1)
    return metrics


def write_to_csv(metrics_dict, all_keys, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Metric'] + list(metrics_dict.keys())
        writer.writerow(header)

        for key in all_keys:
            row = [key]
            for file in metrics_dict:
                row.append(metrics_dict[file].get(key, ''))
            writer.writerow(row)

    
def log_error(err_msg):
    
    with open("/home/mcallisl/perf_automation/log-dev1.txt", "a") as f:
        f.write(err_msg)
        f.write("\n\n\n")
        f.close()
    

def log_experiment(exp_str, time_str, args):

    with open("/home/mcallisl/perf_automation/log-dev1.txt", "a") as f:
        
        f.write("-----------------------------------------------------------------------------------------------\n")
        f.write(time_str)
        f.write("\n\n")
        
        f.write("experiment command")
        f.write(exp_str)
        f.write("\n\n")
        
        f.write("isa: ")
        f.write(args[0])
        f.write("\n\n")
        
        f.write("cpu: ")
        f.write(args[1])
        f.write("\n\n")
        
        f.write("mem: ")
        f.write(args[2])
        f.write("\n\n")
        
        f.write("cache: ")
        f.write(args[3])
        f.write("\n\n")
        
        f.write("cores: ")
        f.write(args[4])
        f.write("\n\n")
        
        f.write("work: ")
        f.write(args[5])
        f.write("\n\n")
        
        f.write("perf: ")
        f.write(args[6])
        f.write("\n")
        
        f.write("-----------------------------------------------------------------------------------------------")
        f.write("\n\n\n")
        
        f.close()
    
    
    
if __name__=="__main__":
    main()