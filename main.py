import argparse
import os
import shutil
import time

def sync_folders(src_folder, dst_folder, interval, log_file):
    while True:
        # Log the start time of the synchronization
        log_text = f"Started synchronization at {time.ctime()}\n"
        print(log_text)
        with open(log_file, 'a') as log:
            log.write(log_text)

        # Iterate through all files and directories in the source folder
        for root, dirs, files in os.walk(src_folder):
            dst_dir = root.replace(src_folder, dst_folder)

            # Create the destination directory if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
                log_text = f"Created directory: {dst_dir}\n"
                print(log_text)
                with open(log_file, 'a') as log:
                    log.write(log_text)

            # Copy or update files in the destination directory
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)

                # Copy the file if it does not exist or has been modified
                if not os.path.exists(dst_file) or \
                    (os.path.getmtime(src_file) - os.path.getmtime(dst_file)) > 1:
                    shutil.copy2(src_file, dst_file)
                    log_text = f"Copied file: {src_file} -> {dst_file}\n"
                    print(log_text)
                    with open(log_file, 'a') as log:
                        log.write(log_text)

            # Remove any files or directories in the destination directory that do not exist in the source directory
            for item in os.listdir(dst_dir):
                src_item = os.path.join(root, item)
                dst_item = os.path.join(dst_dir, item)

                if not os.path.exists(src_item):
                    if os.path.isfile(dst_item):
                        os.remove(dst_item)
                        log_text = f"Removed file: {dst_item}\n"
                    else:
                        shutil.rmtree(dst_item)
                        log_text = f"Removed directory: {dst_item}\n"
                    print(log_text)
                    with open(log_file, 'a') as log:
                        log.write(log_text)

        # Log the end time of the synchronization
        log_text = f"Finished synchronization at {time.ctime()}\n\n"
        print(log_text)
        with open(log_file, 'a') as log:
            log.write(log_text)

        # Sleep for the specified interval
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize two folders')
    parser.add_argument('src_folder', type=str, help='The source folder')
    parser.add_argument('dst_folder', type=str, help='The destination folder')
    parser.add_argument('--interval', type=int, default=60, help='The synchronization interval in seconds')
    parser.add_argument('--log', type=str, default='sync.log', help='The log file')
    args = parser.parse_args()

    sync_folders(args.src_folder, args.dst_folder, args.interval, args.log)
