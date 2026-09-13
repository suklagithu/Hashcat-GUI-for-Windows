# Hashcat GUI for Windows

A simple graphical user interface for Hashcat built with Python and PyQt5.

## Features

- Simple graphical interface for Hashcat
- Hash mode selection
- Wordlist selection
- Automatic hash mode detection
- Hashcat output and status display
- Password recovery progress monitoring
- Case-based output organization
- CPU and GPU-based Hashcat workloads

## Installation

Follow these steps to install and run Hashcat GUI on Windows.

### 1. Install Python

Install the latest version of Python for Windows:

https://www.python.org/downloads/

During installation, make sure **Add Python to PATH** is enabled.

Verify the installation:

```cmd
python --version
```

### 2. Download Hashcat

Download the latest **Windows binary release** of Hashcat:

https://hashcat.net/hashcat/

**Important:** Download the Windows binary release, not the source code.

Extract the downloaded Hashcat archive.

For example:

```text
C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2
```

The extracted folder should contain files such as:

```text
hashcat.exe
hashcat.bin
OpenCL\
rules\
masks\
```

### 3. Copy the GUI into the Hashcat folder

Download `hashcat_gui.py` from this repository.

Copy `hashcat_gui.py` into the same folder where `hashcat.exe` is located.

The folder should look like:

```text
hashcat-7.1.2\
├── hashcat.exe
├── hashcat.bin
├── hashcat_gui.py
├── OpenCL\
├── rules\
└── ...
```

**Important:** Keep `hashcat_gui.py` inside the Hashcat folder. Do not move or delete the `OpenCL` folder or other required Hashcat files.

### 4. Install the required Python library

Open Command Prompt and navigate to your Hashcat folder:

```cmd
cd "C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2"
```

Install the required library:

```cmd
python -m pip install -r requirements.txt
```

### 5. Add Hashcat to Windows PATH

Add the folder containing `hashcat.exe` to your Windows **PATH** environment variable.

Example:

```text
C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2
```

After adding it to PATH, close Command Prompt and open a **new** Command Prompt.

Verify Hashcat:

```cmd
hashcat --version
```

You should see the installed Hashcat version.

You can also check available CPU and GPU devices:

```cmd
hashcat -I
```

### 6. Run the GUI

From the Hashcat folder, run:

```cmd
python hashcat_gui.py
```

The Hashcat GUI should now open.

## Desktop Shortcut

You can create a Windows desktop shortcut to launch the GUI without opening Command Prompt.

Right-click the desktop and select:

**New → Shortcut**

Use the following as the shortcut target:

```text
"C:\Users\YourName\AppData\Local\Programs\Python\Python311\pythonw.exe" "C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2\hashcat_gui.py"
```

Replace `YourName` with your Windows username.

After creating the shortcut, open:

**Right-click shortcut → Properties**

Set **Start in** to your Hashcat folder:

```text
C:\Users\YourName\Downloads\hashcat\hashcat-7.1.2
```

The **Start in** location is important because the GUI needs to access Hashcat and its required files.

The repository also includes:

```text
hashcat_gui_icon.ico
```

which can be used as the shortcut icon.

## Supported Hash Modes

| Hash Type | Hashcat Mode |
|---|---:|
| WPA/WPA2 | 22000 |
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| NTLM | 1000 |
| bcrypt | 3200 |

## Output

The GUI automatically creates case folders in the user's Downloads directory:

```text
Downloads\
├── case1\
├── case2\
├── case3\
└── ...
```

Each case contains the corresponding Hashcat output log.

Converted `.hc22000` files are stored in:

```text
C:\Users\YourName\.hashcat_suite_converted\
```

## GPU Support

Hashcat can use supported CPU and GPU devices.

Check available devices:

```cmd
hashcat -I
```

Run a benchmark:

```cmd
hashcat -b
```

GPU performance depends on your hardware, drivers, and supported compute runtime.

## Troubleshooting

### Python is not recognized

Make sure Python is installed and **Add Python to PATH** was enabled during installation.

### PyQt5 is missing

Run:

```cmd
python -m pip install PyQt5
```

### Hashcat is not recognized

Make sure the folder containing `hashcat.exe` has been added to Windows PATH.

Then open a new Command Prompt and run:

```cmd
hashcat --version
```

### Hashcat is not found by the GUI

Make sure `hashcat_gui.py` and `hashcat.exe` are in the same Hashcat folder.

### OpenCL folder error

Make sure the `OpenCL` folder still exists inside the Hashcat installation directory and that the GUI is being launched with the Hashcat folder as its **Start in** directory.

## Important

Hashcat is **not included** in this repository.

Download Hashcat separately from the official Hashcat website:

https://hashcat.net/hashcat/

Do not upload Hashcat binaries, wordlists, capture files, password databases, hashes, or other sensitive data to this public repository.

## Disclaimer

This project is intended for educational purposes, authorized security testing, password recovery, digital forensics, and security research.

Only use Hashcat against systems, accounts, networks, and data that you own or have explicit permission to test.

The author is not responsible for misuse of this software.
