import requests
from pathlib import Path
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)

def get_token(credential_set: str) -> str:
    """
    return token string
    check for existing valid token in token file
    if the file does not exist or the token is out of date, create token
    """

    token_file = Path(f"{credential_set}.token.file")
    if token_file.is_file():
        time_issued, sessiontoken = token_file.read_text().split("\n")
        # tokens are valid for 500 seconds
        if time.time() - float(time_issued) < 500:
            return sessiontoken

    return create_token(credential_set, token_file)


def create_token(credential_set: str, token_file: Path) -> str:
    """
    request token string based on credentials
    write time and token to a file and return token
    """
    user, pw, tenant = credential_set
    # build the query string and get a new token
    url = "https://nypl.preservica.com/api/accesstoken/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"username={user}&password={pw}&tenant={tenant}"
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()

    if not data["success"]:
        logging.error("Token did not generate successfully")

    # write token to token.file for later reuse
    token_file.write_text(f'{str(time.time())}\n{data["token"]}')

    return data["token"]

def post_so_api(uuid: str, accesstoken: str) -> requests.Response:
    """Make a POST request to the export Structural Object endpoint"""
    export_so_url = f"https://nypl.preservica.com/api/entity/structural-objects/{uuid}/exports"
    export_headers = {
        "Preservica-Access-Token": accesstoken,
        "Content-Type": "application/xml;charset=UTF-8",
    }

    xml_str = "<ExportAction xmlns=\"http://preservica.com/EntityAPI/v7.0\" xmlns:xip=\"http://preservica.com/XIP/v7.0\">" \
                                + "<IncludeContent>Content</IncludeContent>" \
                                + "<IncludeMetadata>Metadata</IncludeMetadata>" \
                                + "<IncludedGenerations>All</IncludedGenerations>" \
                                + "<IncludeParentHierarchy>false</IncludeParentHierarchy>" \
                                + "</ExportAction>"
    # make the API call
    post_response = requests.post(export_so_url, headers=export_headers, data=xml_str)

    return post_response

def get_progress_api(progresstoken, accesstoken) -> requests.Response:
    """Make a GET request to check progress of the export request"""
    check_progress_url = f"https://nypl.preservica.com/api/entity/progress/{progresstoken}?includeErrors=true"

    get_progress_headers = {
        "Preservica-Access-Token": accesstoken,
        "accept": "application/xml;charset=UTF-8"
    }
    # make the API call
    get_progress_response = requests.get(check_progress_url, headers=get_progress_headers)

    return get_progress_response

def get_export_download_api(progresstoken, accesstoken):
    """Make a GET request to download the package"""
    get_export_url = f"https://nypl.preservica.com/api/entity/actions/exports/{progresstoken}/content"

    get_export_headers = {
        "Preservica-Access-Token": accesstoken,
        "accept": "application/octet-stream",
        "Content-Type": "application/xml;charset=UTF-8"
        }
    get_progress_response = requests.get(get_export_url, headers=get_export_headers)

    return get_progress_response

def main():

    # generate token
    user = input("Enter user name: ")
    pw = input("Enter password: ")
    tenant = input("Enter tenant (nypl or nypltest)")

    credential_set = (user, pw, tenant)

    accesstoken = get_token(credential_set)
    so_uuid = "85fa0068-f63b-49fc-8310-e0e11944c45a"

    post_response = post_so_api(so_uuid, accesstoken)

    # checking for API status code
    if post_response.status_code == 202:
        logging.info(f"Progress token: {post_response.text}")
        progresstoken = post_response.text
        time.sleep(10)
    else:
        logging.error(f"POST request unsuccessful: code {post_response.status_code}")
        sys.exit(0)

    # checking for API status code for 15 times. with 5 secs interval
    for _ in range(15):
        time.sleep(5)
        get_progress_response = get_progress_api(progresstoken, accesstoken)
        if get_progress_response.status_code != 200:
            logging.error(f"""GET progress request unsuccessful:
                          code {get_progress_response.status_code}""")
            return
        else:
            logging.info(f"Progress completed. Will proceed to download")
            time.sleep(60)
            get_export_request = get_export_download_api(progresstoken, accesstoken)
            # checking for API status code
            if get_export_request.status_code == 200:
                logging.info(f"The exported content is in the process of being downloaded")
                # save the file
                save_file = open(f"{so_uuid}.zip", "wb")  # wb: write binary
                save_file.write(get_export_request.content)
                save_file.close()
            else:
                logging.error(f"Get export request unsuccessful: {get_export_request.status_code}")



if __name__ == "__main__":
    main()