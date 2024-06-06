# Danbooru-Import-Scripts

These scripts are made to import artists from danbooru and upload them to a selfhosted danbooru site, these scripts are not to be used to clone danbooru and are purely for self hosted personal sites.

### artists-manual.py 

This is for imprting a single artist at a time using the artist ID ``https://danbooru.donmai.us/artists/ID``, however the script will keep running waiting for the next ID until you press ``Ctrl+C``

the output of this will look like below

```bash
python3 artists-manual.py
Login to Danbooru successful.
Login to my_site successful.
Enter the artist ID to search for (or press Ctrl+C to exit): 205113
Processing artist 205113, URL: https://www.pixiv.net/users/8279562
Processing artist 205113, URL: https://twitter.com/micon40124147
Processing artist 205113, URL: https://twitter.com/intent/user?user_id=1259809228035813378
Processing artist 205113, URL: https://sketch.pixiv.net/@final-fantasy-leo
Processing artist 205113, URL: https://www.pixiv.net/stacc/final-fantasy-leo
Successfully updated artist: micon
Enter the artist ID to search for (or press Ctrl+C to exit): 
```

### artists.py 

This is for importing your api limit of pages of random artists from danbooru (im not 100% sure how the api decides what artists to provide info for i think it goes by the most recently updated) this script will run automatically and will process pages untill you reach your api limit once you reach your API limit it will then start uploading the proccessed pages to your site

the output will look like below but will continue untill the api limit has been reached, once the script has completed it will automatically exit
i suggest running this script in a screened terminal so you can detach from the screen and keep it running

```bash
python3 artists.py
Login to Danbooru successful.
Login to my_site successful.
Processing artist page 1
Processing artist page 2
Processing artist page 3
Processing artist page 4
Processing artist page 5
Processing artist page 6
Processing artist page 7
Processing artist page 8
Processing artist page 9
Processing artist page 10
Processing artist page 11
Processing artist page 12
Processing artist page 13
Processing artist page 14
Processing artist page 15
Processing artist page 16
```

### tags.py 

This will get upto 1000 Pages of tags from your site and then search danbooru for these tags and the update them with the details from danbooru such as if the tag is a "copy:", "char:", "meta:" etc tag

see below for sample output

```bash
Processing tag page 402
Processing tag page 403
Processing tag page 404
Processing tag page 405
Processing tag page 406
Processing tag page 407
Processing tag page 408
Updated tag ookami_mio_(another_ookami_mio) successfully.
Updated tag miofa_(ookami_mio) successfully.
Updated tag micon successfully.
Updated tag wolf_tail successfully.
Updated tag wolf_girl successfully.
Updated tag ookami_mio successfully.
Updated tag pink_shorts successfully.
Updated tag partially_colored successfully.
```

## Setup

### Step 1 - Install Python

Make sure you have Python 3.10 or higher installed:

```
sudo apt install python3
```

### Step 2 - Download Project Files

Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/Amateur-God/Danbooru-Artist-Importer/releases

I reccomend extracting the files into its own directory in opt like "/opt/BooruScripts"

### Step 3 - Set up and run

#### Install requirements

navigate to the directory where you have the script

if in reccomended directory

```
cd /opt/BooruScripts
```

```
pip install -r requirements.txt
```

#### Edit Env Variables

Open config.env in the config Folder with your prefered text editor and Replace the placeholders with the correct variables

if installed in its own folder in /opt

```
sudo nano /opt/BooruScripts/config/config.env
```

```py
YOUR_DANBOORU_SITE = 'https://www.your-site.com'

# Credentials for Danbooru
DANBOORU_USERNAME = 'username'
DANBOORU_API_KEY = 'api_key'

# Credentials for Your Site
SITE_USERNAME = 'username'
SITE_API_KEY = 'api_key'
``` 

#### Run on linux

This assumes you moved the script files to their own folder in opt

```bash
sudo chmod a+x /opt/BooruScripts/*
```

```bash
cd /opt/BooruScripts
```

```bash
python3 script-name.py
```