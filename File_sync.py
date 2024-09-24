import os
import hashlib
import shutil
import time
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()



def copy_file(source_file, replica_file):
    shutil.copy2(source_file, replica_file)
    log_operation(f"Created file: {source_file} -> {replica_file}")



def update_file(source_file, replica_file):
    shutil.copy2(source_file, replica_file)
    log_operation(f"Updated file: {source_file} -> {replica_file}")



def sync_files(source_dir, replica_dir):
    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)

    with ThreadPoolExecutor() as executor:
        futures = []
        
        for root, dirs, files in os.walk(source_dir):
            relative_path = os.path.relpath(root, source_dir)
            replica_path = os.path.join(replica_dir, relative_path)

            if not os.path.exists(replica_path):
                os.makedirs(replica_path)

            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_path, file)

                source_hash = calculate_hash(source_file)

                if os.path.exists(replica_file):
                    destination_hash = calculate_hash(replica_file)

                    if source_hash != destination_hash:
                        futures.append(executor.submit(update_file, source_file, replica_file))
                    else:
                        log_operation(f"File is unchanged: {file}")
                else:
                    futures.append(executor.submit(copy_file, source_file, replica_file))

                    
        for future in as_completed(futures):
            future.result()



def clean_destination(source_dir, replica_dir):
    with ThreadPoolExecutor() as executor:
        futures = []
        
        for root, dirs, files in os.walk(replica_dir):
            relative_path = os.path.relpath(root, replica_dir)
            source_path = os.path.join(source_dir, relative_path)

            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_path, file)

                if not os.path.exists(source_file):
                    futures.append(executor.submit(os.remove, replica_file))
                    log_operation(f"Removing file: {replica_file}")

            for dir in dirs:
                replica_subdir = os.path.join(root, dir)
                source_subdir = os.path.join(source_path, dir)
 
                if not os.path.exists(source_subdir):
                    futures.append(executor.submit(shutil.rmtree, replica_subdir))
                    log_operation(f"Removing folder: {replica_subdir}")

        
        for future in as_completed(futures):
            future.result()



def log_operation(message):
    print(message)
    logging.info(message)



def periodic_sync(source_dir, replica_dir, interval_seconds):
    while True:
        log_operation("----------------------------------------------------------------------------------------------")
        log_operation(f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
        sync_files(source_dir, replica_dir)
        clean_destination(source_dir, replica_dir)
        time.sleep(interval_seconds)



def main():
    
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_dir")
    parser.add_argument("replica_dir")
    parser.add_argument("interval", type=int)
    parser.add_argument("log_file")
    args = parser.parse_args()

    
    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format = '%(message)s')

    periodic_sync(args.source_dir, args.replica_dir, args.interval)



if __name__ == "__main__":
    main()
