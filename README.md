# Adultwork Private Gallery Downloader

## Installation Instructions 
### Install Selenium Driver
Windows:
```
choco install selenium-gecko-driver
```
Mac OS (not tested):
```
brew install geckodriver
```
Linux (not tested):
```
wget https://api.github.com/repos/mozilla/geckodriver/releases/latest
tar -xvzf geckodriver*
chmod +x geckodriver
export PATH=$PATH:/path-to-extracted-file/. <------change file name
```

### Install Python 3
https://www.python.org/downloads/


### Install environment
```
pip install virtualenv
virtualenv venv
pip install -r requirements.txt
deactivate
```

## Usage Instructions
Windows:
```
.\venv\Scripts\activate
python .\downloader.py
```

1. Enter profile number this can be found in the profile URL.

    e.g. https://www.adultwork.com/ViewProfile.asp?UserID=1234567 <----- Profile Number
2. 1st window will popup, enter your details and login.
3. Private gallery download will begin in the background to the downloads folder where the script is located.


## Troubleshooting
If you encounter any errors please open a GitHub issue with URL, system and error details and I will take a look.
