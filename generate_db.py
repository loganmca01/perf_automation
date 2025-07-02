import sqlite3

workload_names = [
    "TopdownL1",
    "tma_frontend_bound_group",
    "tma_backend_bound_group",
    "tma_fetch_latency_group",
    "tma_fetch_bandwidth_group",
    "tma_memory_bound_group",
    "tma_core_bound_group",
]

create_index = "CREATE TABLE "

try:
    with sqlite3.connect(":memory:") as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        
        cursor = conn.cursor()
        
        
        
        

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)