import sqlite3
import csv
import os

workload_names = [
    "TopdownL1",
    "tma_frontend_bound_group",
    "tma_backend_bound_group",
    "tma_fetch_latency_group",
    "tma_fetch_bandwidth_group",
    "tma_memory_bound_group",
    "tma_core_bound_group",
]

create_index = """
CREATE TABLE experiment_index (
    datetime INTEGER NOT NULL,
    device_name TEXT NOT NULL,
    isa TEXT NOT NULL,
    cpu TEXT NOT NULL,
    memsize TEXT NOT NULL,
    l1 TEXT NOT NULL,
    l2 TEXT NOT NULL,
    l3 TEXT NOT NULL,
    cores INTEGER NOT NULL,
    workload TEXT NOT NULL,
    event_group TEXT NOT NULL,    
    PRIMARY KEY (datetime, device_name)
);
"""

create_topdownl1 = """
CREATE TABLE topdownl1 (
    datetime INTEGER NOT NULL,
    device_name TEXT NOT NULL,
    tma_frontend_bound REAL NOT NULL,
    tma_bad_speculation REAL NOT NULL,
    tma_retiring REAL NOT NULL,
    tma_backend_bound REAL NOT NULL,
    time_elapsed REAL NOT NULL,
    total_uops INTEGER NOT NULL,
    PRIMARY KEY (datetime, device_name)
);
"""

ISA = 0
CPU = 1
MEM = 2
CACHE = 3
CORES = 4



def import_file(filename, cursor):
    
    no_ext = filename.split(".")[0]
    info = no_ext.split("-")
    
    

    
    
    

try:
    with sqlite3.connect(":memory:") as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        
        cursor = conn.cursor()
        
        cursor.execute(create_index)
        cursor.execute(create_topdownl1)
        
        test = cursor.execute("SELECT name FROM sqlite_master")
        print(test.fetchall())
        
        for filename in os.listdir("./extracted_csvs/"):
            
            import_file(filename, cursor)
        
            
        
        
        

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)