# URL Converter

URL Converter is a Python application with a graphical user interface (GUI) built using PyQt5. It allows users to sanitize and unsanitize URLs, converting them between normal and obfuscated formats for security purposes.

## Features

- **Sanitize URLs**: Convert normal URLs into a sanitized format by replacing `.` with `[.]` and `http` with `hXXp`, preventing accidental clicks or link detection.
- **Unsanitize URLs**: Convert sanitized URLs back to their normal form for easy access.
- **Batch Processing**: Handle multiple URLs at once.
- **User-Friendly Interface**: Simple GUI with clear buttons for sanitizing, unsanitizing, and clearing text.

## Requirements

- **Operating System**: Windows 7 or later (64-bit) for the executable
- **Python 3.x** and **PyQt5** (if running from source code)

## Installation

### Download and Run the Executable

You can download a pre-built executable of URL Converter for Windows from the [Releases](https://github.com/s-pillow/url-converter/releases) page.

1. **Download the Executable**

   - Go to the Releases page and download the `url_converter.exe` file.

2. **Run the Executable**

   - Double-click `url_converter.exe` to launch the application.
   - If you see a SmartScreen warning, click **"More info"** and then **"Run anyway"**.

### Run from Source Code

If you prefer to run the application from the source code or are using a different operating system:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/s-pillow/url-converter.git

