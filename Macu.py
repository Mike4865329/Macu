import json
import urllib.request
import os
import signal
import time
from tqdm import tqdm

def startfunc():
    print("Welcome to Macu! Here's the List of Apps https://macu.xbxonline.repl.co/list.php")
    print("!IMPORTANT! : ALL of the apps are community submitted. please contact me at https://macu.xbxonline.repl.co/contact.php when you find a virus. ")
    print("Thanks for Using my app! You can support users by adding an app here: https://macu.xbxonline.repl.co/addanapp.html?ap")
    app_name_or_id = input("Enter the name or app id of the app you want to download: ")
    try:
        download_latest_version(app_name_or_id)
    except KeyError:
        print(f"Error: {app_name_or_id.capitalize()} is not found in the database for downloading.")
        startfunc()
    except Exception as e:
        print(f"Error occurred while downloading: {str(e)}")
        time.sleep(3)

def signal_handler(signal, frame):
    print('\nCtrl + C Going back....')
    time.sleep(1)
    startfunc()

signal.signal(signal.SIGINT, signal_handler)

def get_latest_version(app_name_or_id):
    with urllib.request.urlopen(f'https://macu.xbxonline.repl.co/app/list/win.json') as url:
        data = json.loads(url.read().decode())
    if app_name_or_id.isdigit():
        for app in data.values():
            if app['appid'] == app_name_or_id:
                return app
        raise KeyError
    else:
        return data[app_name_or_id]

def download_latest_version(app_name_or_id):
    app = get_latest_version(app_name_or_id.lower())
    name = app['name'].replace(' ', '_')
    version = app['version'].replace(' ', '_')
    url = app['url']
    description = app['description']
    author = app['author']
    license = app['license']
    tags = ', '.join(app['tags'])
    appid = app['appid']
    fileext = app['file_ext']
    filesize_app = app['file_size']
    
    print(f"Name: {name}")
    print(f"Version: {version}")
    print(f"Description: {description}")
    print(f"Author: {author}")
    print(f"License: {license}")
    print(f"Tags: {tags}")
    print(f"App ID: {appid}")
    print(f"File Size: {filesize_app}")
    
    choice = input("Do you want to Download and install now? [Y]es or [N]o: ")
    if choice.lower() == "y":
        try:
            print(f"Preparing {name} {version}... (This may take a moment.)")
            with urllib.request.urlopen(url) as u, open(f"{name}_{version}.{fileext}", 'wb') as f:
                meta = u.info()
                file_size = int(meta.get_all("Content-Length")[0])
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = f"[{int(file_size_dl * 100 / file_size)}% {'====' * int(file_size_dl * 20 / file_size):80s}]"
                    print(f"\r{status}", end='', flush=True)
            print(f"\nDownload complete!")
            time.sleep(1)
            os.startfile(f"{name}_{version}.{fileext}")
            startfunc()
        except Exception as e:
            print(f"Error occurred while downloading: {str(e)}")
            time.sleep(3)
    else:
        print("Download aborted.")
        time.sleep(3)
        startfunc()


if __name__ == "__main__":
   startfunc()
