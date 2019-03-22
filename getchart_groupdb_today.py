import requests
import gzip
import config
import utils
import os

# CODE FROM https://stackoverflow.com/a/39225039
# CODE FROM https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

# CODE FROM https://stackoverflow.com/a/39225039
# CODE FROM https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

# CODE FROM https://stackoverflow.com/a/39225039
# CODE FROM https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def main():
    localconfig=config.config['EXTERNAL']
    filename=""
    latestdate="0"
    latestid=""
    date="0"

    # get file list of root folder
    r=requests.get("https://www.googleapis.com/drive/v3/files"+"?q='"+localconfig['gdriveroot']+"'+in+parents&key="+localconfig['gdrivekey'])
    rootdir=r.json()['files']
    
    for item in rootdir:
        if item['mimeType'] == "application/vnd.google-apps.folder":
            #dates[item['name']]=item['id']
            try:
                if int(item['name']) > int(date):
                    latestdate=item['name']
                    latestid=item['id']
                    date=item['name']
                pass
            except TypeError:
                # since there are other folders
                pass
            except ValueError:
                # since there are other folders
                pass

    # latest date name/id = latestdate
    # latest date's folder = latestid

    # get list of all the files in the latest dir
    r2=requests.get("https://www.googleapis.com/drive/v3/files"+"?q='"+latestid+"'+in+parents&key="+localconfig['gdrivekey'])
    datedir=r2.json()['files']
    if not os.path.exists(localconfig['localfoldergz']+latestdate):
        os.makedirs(localconfig['localfoldergz']+latestdate)
    if not os.path.exists(localconfig['localfolder']+latestdate):
        os.makedirs(localconfig['localfolder']+latestdate)
        
    # download all the files to input/gzip/yyyymmdd
    for item in datedir:
        download_file_from_google_drive(item['id'], localconfig['localfoldergz']+latestdate+"/"+item['name'])

        # ungzip the csv.gz in input/gzip/yyyymmdd/*.csv.gz to input/yyyymmdd/*.csv
        with gzip.open(localconfig['localfoldergz']+latestdate+"/"+item['name'],'rt') as f:
            with open(localconfig['localfolder']+latestdate+"/"+item['name'][:-3],'w') as f2:
                for line in f:
                    f2.write(line)
    

# Run main()
if __name__ == "__main__":
    main()
