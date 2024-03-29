import os
import time
import socket
from zeroconf import ServiceInfo, Zeroconf

class FileSyncService:
    def __init__(self, directory):
        self.directory = directory
        self.files = set()

    def sync_files(self):
        current_files = set(os.listdir(self.directory))
        new_files = current_files - self.files
        deleted_files = self.files - current_files

        # Implement rsync logic here to sync new and deleted files

        self.files = current_files

    def run(self):
        while True:
            self.sync_files()
            time.sleep(5)  # Sync every 5 seconds

def register_zeroconf_service(directory, port):
    zeroconf = Zeroconf()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    info = ServiceInfo("_file-sync._tcp.local.",
                       f"{hostname}._file-sync._tcp.local.",
                       socket.inet_aton(local_ip), port, 0, 0,
                       {"path": directory})
    zeroconf.register_service(info)

    print(f"File Sync Service registered at {hostname}:{port}")

    try:
        input("Press Enter to exit...\n\n")
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()

if __name__ == "__main__":
    directory_to_sync = "./syncFolder"
    sync_service = FileSyncService(directory_to_sync)
    
    # Start file sync service
    sync_service.run()

    # Register Zeroconf service
    register_zeroconf_service(directory_to_sync, 5555)
