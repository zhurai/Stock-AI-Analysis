import requests
import gzip
import config


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

# Download csv.gz and write a new file
def main():
    # download the csv.gz from google drive
    download_file_from_google_drive(config.gdrivecsvid, config.inputfile+".gz")

    # write the new file per line in gzip
    with gzip.open(config.inputfile+".gz",'rt') as f:
        with open(config.inputfile,'w') as f2:
            for line in f:
                f2.write(line)

# Run main()
main()
