# Hashcat GUI for Windows

A simple Windows GUI for [Hashcat](https://hashcat.net/hashcat/) built with Python and PyQt5.

## Features

- Hash mode selection
- Wordlist selection
- Automatic hash mode detection
- Hashcat output and status monitoring
- CPU and GPU support
- Case-based output organization
- Windows desktop shortcut support

## Installation

### 1. Install Python

Install the latest Python version for Windows:

https://www.python.org/downloads/

During installation, enable **Add Python to PATH**.

Verify:

```cmd
python --version
```

### 2. Download Hashcat

Download the latest **Windows binary release** of Hashcat:

https://hashcat.net/hashcat/

Extract the archive. Do **not** download the source code.

### 3. Place the GUI in the Hashcat folder

Copy `hashcat_gui.py` into the same folder as `hashcat.exe`.

Example:

```text
hashcat-7.1.2\
├── hashcat.exe
├── hashcat.bin
├── hashcat_gui.py
├── OpenCL\
└── ...
```

Keep the `OpenCL` folder and other Hashcat files in their original locations.

### 4. Install PyQt5

Open Command Prompt in the Hashcat folder and run:

```cmd
python -m pip install -r requirements.txt
```

### 5. Add Hashcat to PATH

Add the folder containing `hashcat.exe` to your Windows **PATH**.

Example:

```text
C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2
```

Open a **new** Command Prompt and verify:

```cmd
hashcat --version
```

### 6. Run the GUI

From the Hashcat folder:

```cmd
python hashcat_gui.py
```

## Desktop Shortcut

Create a Windows desktop shortcut using `pythonw.exe`.

Example Target:

```text
"C:\Users\YourName\AppData\Local\Programs\Python\Python311\pythonw.exe" "C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2\hashcat_gui.py"
```

Set **Start in** to:

```text
C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2
```

The repository also includes `hashcat_gui_icon.ico`, which can be used as the shortcut icon.

## Supported Hash Modes

| Hash Type | Mode |
|---|---:|
| WPA/WPA2 | 22000 |
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| NTLM | 1000 |
| bcrypt | 3200 |

## GPU Support

Check available devices:

```cmd
hashcat -I
```

Run a benchmark:

```cmd
hashcat -b
```

GPU performance depends on your hardware and installed drivers.

## Output

The GUI creates case folders in your Downloads directory:

```text
Downloads\
├── case1\
├── case2\
└── ...
```

Converted `.hc22000` files are stored in:

```text
C:\Users\YourName\.hashcat_suite_converted\
```

## Important

Hashcat is **not included** in this repository. Download it separately from the official Hashcat website:

https://hashcat.net/hashcat/

Do not upload private credentials, sensitive hashes, capture files, or other sensitive data to this public repository.

## Disclaimer

This project is intended for educational purposes, authorized security testing, password recovery, digital forensics, and security research.

Only use Hashcat against systems and data that you own or have explicit permission to test.
