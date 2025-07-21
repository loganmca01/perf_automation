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
MEMSIZE = 2
CACHE = 3
CORES = 4
#TODO


def insert_topdownl1(filename, cursor):
    
    
def insert_index(filename, cursor, datetime):
    no_ext = filename.split(".")[0]
    info = no_ext.split("-")

    index_insert = "INSERT INTO experiment_index (datetime,device_name,isa,cpu,memsize,l1,l2,l3,cores,workload,event_group) VALUES ("
    index_insert += datetime + ","
    index_insert += info[DEVICE_NAME] + ","
    index_insert += info[ISA] + ","
    index_insert += info[CPU] + ","
    index_insert += info[MEMSIZE] + ","
    index_insert += info[L1] + ","
    index_insert += info[L2] + ","
    index_insert += info[L3] + ","
    index_insert += info[CORES] + ","
    index_insert += info[WORKLOAD] + ","
    index_insert += info[EVENT_GROUP]
    
    cursor.execute(index_insert)

def import_file(filename, cursor):

    reader = csv.reader(filename)
    
    entries = []
    for i in range(0,10):
        entries[i] = []
        
    i = 0;
    while (row = next(reader)):
        for entry in row[1:]:
            entries[i].append(entry)
            i = i + 1
    
    
    
    if (info[EVENT_GROUP] = "TopdownL1"):
        import_topdownl1(filename, cursor)
    
        
    

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