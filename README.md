# SVN File Information Export Tool

A tool for extracting file information from SVN repositories and generating Excel documents.

## Features
- Support for SVN repository file information extraction (including filename, path, version number, author, commit time, etc.)
- Graphical user interface, simple and intuitive operation
- File format filtering support (selective export of specific file types)
- Subdirectory recursive scanning
- Automatic history saving (SVN URLs, username, etc.)
- Real-time execution progress and log information display
- Enter key quick execution support
- Multi-language support (English/Chinese)

## System Requirements
- Windows operating system
- [TortoiseSVN](https://tortoisesvn.net/downloads.html) (command line tools must be installed)
  - Check "command line client tools" during installation
  - Add SVN command line tools to system PATH after installation

## Usage
1. Run the program (double-click the exe file)
2. Enter the following information:
   - SVN repository URL
   - Username and password
   - File format filter (optional, e.g.: *.dwg;*.dxf;*.xlsx)
   - Excel save location
3. Click "Start Export" or press Enter to execute
4. Wait for completion and check results

## Development Environment
- Python 3.8+
- PySide6 (Qt for Python)
- openpyxl (Excel processing)

## Build Instructions
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Execute packaging:
```bash
pyinstaller build.spec
```

## Notes
1. Ensure TortoiseSVN and its command line tools are properly installed before first use
2. If you encounter "SVN command line tool not detected" error, please check:
   - Whether TortoiseSVN is installed
   - Whether command line tools were checked during installation
   - Whether SVN command line tool path is included in system PATH
3. File format filter supports wildcard (*) matching
4. All input fields (except password) automatically save last used values
5. SVN URL supports history, saving the 10 most recently used addresses