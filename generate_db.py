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
    datetime TEXT NOT NULL,
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
    datetime TEXT NOT NULL,
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

#constants for locations within filename
ISA = 0
CPU = 1
MEMSIZE = 2
CACHE = 3
CORES = 4
WORKLOAD = 5
EVENT_GROUP = 6
DEVICE_NAME = 7

#constants for locations within csv
DATETIME = 1
TIME_ELAPSED = 3
TMA_BACKEND_BOUND = 4
TMA_BAD_SPECULATION = 5
TMA_FRONTEND_BOUND = 6
TMA_RETIRING = 7
TOTAL_UOPS = 8



def insert_topdownl1(entry, cursor):
    test = 0
    
def insert_index(info, cursor, entry):
    
    cache_sizes = info[CACHE].split(":")

    index_insert = "INSERT INTO experiment_index (datetime,device_name,isa,cpu,memsize,l1,l2,l3,cores,workload,event_group) VALUES ("
    index_insert += "'" + entry[DATETIME] + "'" + ","
    index_insert += "'" + info[DEVICE_NAME] + "'" + ","
    index_insert += "'" + info[ISA] + "'" + ","
    index_insert += "'" + info[CPU] + "'" + ","
    index_insert += "'" + info[MEMSIZE] + "'" + ","
    index_insert += "'" + cache_sizes[0] + "'" + ","
    index_insert += "'" + cache_sizes[1] + "'" + ","
    
    if (len(cache_sizes) == 3):
        index_insert += "'" + cache_sizes[2] + "'" + ","
    else:
        index_insert += "'" + "none" + "'" + ","
    index_insert += info[CORES] + ","
    index_insert += "'" + info[WORKLOAD] + "'" + ","
    index_insert += "'" + info[EVENT_GROUP] + "'"
    index_insert += ");"
    
    print(index_insert)
    
    cursor.execute(index_insert)

def import_file(filename, cursor):

    full_filepath = "./extracted_csvs/" + filename
    
    with open(full_filepath, newline='') as csvfile:
    
        reader = csv.reader(csvfile)
    
        entries = []
        for i in range(0,10):
            entries.append([])
        
        i = 0;
        for row in reader:
            print(row)
            for entry in row[1:]:
                entries[i].append(entry)
                i = i + 1
            i = 0
    
        print(entries)
    
        no_ext = filename.split(".")[0]
        info = no_ext.split("-")
        
        
        
        for entry in entries:
            insert_index(info, cursor, entry)
            
            if (info[EVENT_GROUP] == "TopdownL1"):
                insert_topdownl1(entry, cursor)
            
    
    
    
        
    


#TODO: make whole shell for database access, commands: help, list, view, etc.
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