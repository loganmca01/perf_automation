import run_batch


times = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

time_iter = 0
dev_name = "turing302"

run_batch.extract_data("/home/mcallisl/perf_automation/output_files/ARM-O3-2GiB-128KiB:1024KiB-4-boot-exit-TopdownL1/2025-07-15-14-55-58-turing302", "ARM-O3-2GiB-128KiB:1024KiB-4-boot-exit-TopdownL1-turing302-2025-07-15-14-55-58.csv", times)