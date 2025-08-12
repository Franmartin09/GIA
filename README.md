# GIA (Git AI Commit Assistant)

**GIA** is a lightweight, cross-platform command-line tool for Bash and Windows that analyzes changes in your folder or Git repository and leverages an AI model to generate clear, concise, and contextual commit messages automatically.
Use the command `gai -a` to stage all changes and create a commit with an intelligent summary of all modifications detected.

---

## Installation & Setup

### 1. Install Dependencies

```bash
pip install google-generativeai
```

### 2. Configure Your API Key

* **Linux/macOS:**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

* **Windows PowerShell:**

```powershell
setx GEMINI_API_KEY "your_api_key_here"
```

> ⚠️ **Important:** After setting the environment variable, restart your terminal or open a new session for the changes to take effect.

### 3. Make the Script Executable and Accessible

* **Linux/macOS:**

```bash
chmod +x gai.py
sudo mv gai.py /usr/local/bin/gai
```

* **Windows:**

Save `gai.py` in a directory included in your system’s `PATH`, or add the folder containing `gai.py` to your `PATH` environment variable:

```powershell
setx PATH "$($env:PATH);E:\Proyectos\GIA"
```

> ⚠️ Remember to restart your terminal after modifying the `PATH`.

---

## Usage Examples

* **Stage all changes and create a commit:**

```bash
gai -a
```

* **Stage a specific file and create a commit:**

```bash
gai -f filename.py
```

---

## Additional Information

* GIA uses the Gemini AI model to generate commit messages based on your Git diffs.
* Make sure Git is installed and that you run the tool inside a valid Git repository.
* On Windows, you can create a `.bat` wrapper to call `gai.py` directly using the `gai` command.

---

## Creating a `.bat` Wrapper for Windows

To run `gai.py` easily by typing `gai` from any command prompt:

1. Create a file named `gai.bat` in a folder included in your system’s `PATH` (e.g., the same folder as `gai.py` or another folder in `PATH`).

2. Add the following content to `gai.bat` (adjust the path to your actual location):

```bat
@echo off
python "C:\Path\To\GIA\gai.py" %*
```

* `%*` forwards all provided arguments to the Python script.

3. Save the file.

4. Restart your command prompt or PowerShell.

Now you can run:

```powershell
gai -a
```

or

```powershell
gai -f filename.py
```

---

This wrapper enables seamless usage of the `gai` command without needing to prefix it with `python gai.py`.

---

If you want help automating the setup or have questions, feel free to open an issue or contact the maintainer!