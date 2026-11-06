# NM-Automation: Python task automation and script automation tool

NM-Automation is a terminal workflow automation tool and script automation tool that navigates SCORM course modules on the HCLTech Career Shaper LMS platform. This Python task automation program runs an automated browser workflow from the command line to complete queued training items.

## Architecture

The automation script uses Playwright to drive a Chromium browser. The system has four primary components:

1. Dependency check and browser installation. The script checks for the `playwright` package on startup. If the package is missing, the script installs it using `pip install playwright`. It then executes `playwright install` to install browser binaries.
2. Authentication. The script reads credentials from standard input in the terminal. It launches a Chromium browser with `headless=False` so the user can observe the browser window. It navigates to the login page at `https://hcltech-lms.career-shaper.com/login/index.php`, fills the username and password fields, clicks the two consent checkboxes matching `//span[@class="checkmark"]`, and clicks the Login button. If an alert box matching `//div[@class="alert alert-danger"]` appears, the script terminates.
3. Queue iteration. The script loads the URL list from `links.json`. It iterates through the array and opens each module URL. If the login page reappears, the script reauthenticates and reloads the URL. It inspects the page for `//div[@class="message-box"]` or `//video`. If neither element is visible, the script increments an error counter. If that counter exceeds 3, the loop stops. After each valid navigation step, the script removes the processed URL from the in-memory list.
4. State persistence and error logging. When the loop finishes, the script checks the remaining items in memory. If items remain, the script writes the updated array back to `links.json`. If zero items remain, the script removes `links.json` from disk with `os.remove`. If an unhandled exception occurs, the script writes the exception message to a file named `logs<character>.txt`, where `<character>` is the last character of the exception string, and prints contact details for `connectwithsanthosh@gmail.com`.

## Setup

Install the required Python package and browser binaries:

```bash
pip install playwright
playwright install
```

Ensure `NM AutoMation.py` and `links.json` are present in the same directory.

## Usage

Start the program from your terminal in the directory where `links.json` is located:

```bash
python "NM AutoMation.py"
```

1. Enter your User ID when prompted.
2. Enter your password when prompted.
3. Observe the Chromium browser as it navigates through each module.
4. The script logs total execution time in seconds when it finishes.

## Configuration

The script reads its queue directly from `links.json`:

- Queue format: A JSON array containing target LMS module URLs.
- State file handling: The script removes processed links and writes the remaining list back to `links.json` upon exit. It deletes `links.json` when all items are complete.
- Runtime settings:
  - Headless setting: False. Chromium runs in visible mode.
  - Authentication endpoint: `https://hcltech-lms.career-shaper.com/login/index.php`.
  - Retry cutoff: The script stops after more than 3 unexpected page states.
  - Failure log: Uncaught exceptions write to `logs<character>.txt` in the active directory.
