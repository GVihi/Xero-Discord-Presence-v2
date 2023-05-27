# Xero Discord Presence v2

Show your Discord firends that you're playing Xero! - Now using the Xero API. No more Web Scraping for player info!

## Requirements
- Windows 10 / 11
- Python 3 (https://www.python.org/)

- Packages:
  - requests
  - BeautifulSoup4
  - pypresence

## Setup
1. Download project files
2. Install Python 3
3. Install requirements.txt. Use `python3 -m pip install -r requirements.txt` to install all listed packages
4. Fill out credentials.py with - well, your credentials silly!
- Xero API key and secret must be created over at https://xero.gg/settings/api.
- A Discord App ID can be generated at https://discord.com/developers/applications. 
- It is also important to upload all images from the `assets` folder to your Discord Application over at the `Rich Presence` tab.
5. Run the presence.py script with `python3 presence.py` command

Presence can be stopped via **Keyboard Interrupt** (CTRL + C).


### Discord Presence

![discord](https://github.com/GVihi/Xero-Discord-Presence-v2/blob/main/images/Presence.gif)

## App still in development
The program is still in early development and needs a lot of testing and QoL improvements.
For a fully finished and tested solution, head over to my good friend [Dekirai's GitHub](https://github.com/Dekirai/XeroPresence) and give his tool a try ;D

## Setup Help
Upload all images from the `assets` folder with the `Add Image(s)` button

![Discord_Developer_Portal](https://github.com/GVihi/Xero-Discord-Presence-v2/blob/main/images/Discord%20Developer%20Portal.png)

Create a Xero API key, which will give you the id and secret needed for `credentials.py`

![XERO_API_Key](https://github.com/GVihi/Xero-Discord-Presence-v2/blob/main/images/xero.gg%20API.png)
