# M\*\*6 Levels Please

Need to export m\*\*6 leaderboard leveling data? This is the script for you.

## Prerequisites

1. Python: [download](https://www.python.org/downloads/)
2. Pip: [installation guide](https://pip.pypa.io/en/stable/installation/)
3. A WebDriver that works with your browser
    - [Chrome](https://sites.google.com/chromium.org/driver/?pli=1)
    - [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)
    - [Firefox](https://github.com/mozilla/geckodriver/releases)

## Installation

1. Open your terminal of choice
2. Clone the repository
    ```bash
    git clone https://github.com/JadenLabs/mee6-levels-please.git
    ```
3. Change directory into the cloned repo
    ```bash
    cd mee6-levels-please
    ```
4. Install needed packages
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python main.py [url] [driver]
```

**Options**:

```
  -h, --help     show this help message and exit
  -v, --verbose  Verbose mode for logging
```

#### Example:

```bash
Jaden@JadenLabs ~/Coding/mee6-levels-please
$ python main.py https://mee6.xyz/en/leaderboard/755056745717432350 edge -v
```

After running the script, check the  `/output` folder for the `.json` file.
