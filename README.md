# PySentinel - File Integrity Monitor (FIM)



A professional-grade Python tool to monitor file system integrity using SHA-256 cryptographic hashing.



## Features

- **Baseline Generation**: Create a secure snapshot of a directory.

- **Real-time Detection**: Detects file modifications, deletions, and new file creations.

- **Audit Logging**: All security events are logged in `logs/monitor.log`.

- **Memory Efficient**: Handles large files using chunked hashing.



## Usage

1. **Create Baseline:**

&#x20;  `python src/monitor.py build -d ./target\_folder`



2. **Monitor Integrity:**

&#x20;  `python src/monitor.py monitor -d ./target\_folder`

