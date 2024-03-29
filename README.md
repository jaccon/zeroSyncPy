# File Sync Service with Zeroconf Discovery

## Overview

This project implements a file synchronization service that utilizes Zeroconf (also known as Bonjour or Avahi) for automatic discovery of devices on a local network. The service allows devices within the same network to synchronize files between them without the need for manual configuration.

## Features

- Automatic discovery of devices on the local network using Zeroconf.
- Synchronization of files between discovered devices.
- Simple setup and usage.

## Requirements

- Python 3.x
- Zeroconf library (`zeroconf` or `python-zeroconf`)
- `rsync` installed on devices for file synchronization

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/file-sync-service.git
    ```

2. Install the required Python dependencies:

    ```bash
    pip install zeroconf
    ```

3. Ensure that `rsync` is installed on all devices that will participate in file synchronization.

## Usage

1. Start the file sync service on each device:

    ```bash
    python file_sync_service.py
    ```

2. The service will automatically register itself using Zeroconf and start synchronizing files with other discovered devices.

3. Press Enter to exit the service.

## Configuration

- By default, the service syncs files from the current directory. You can change the directory to sync by modifying the `directory_to_sync` variable in the script.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
