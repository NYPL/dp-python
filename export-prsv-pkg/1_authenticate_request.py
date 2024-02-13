import requests
from pathlib import Path
import time

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
        print("Token did not generate successfully")

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

def main():

    # generate token
    user = input("Enter user name: ")
    pw = input("Enter password: ")
    tenant = input("Enter tenant (nypl or nypltest)")

    credential_set = (user, pw, tenant)

    accesstoken = get_token(credential_set)
    so_uuid = "85fa0068-f63b-49fc-8310-e0e11944c45a"

    post_response = post_so_api(so_uuid, accesstoken)
    print(dir(post_response))
    print(post_response.status_code)

if __name__ == "__main__":
    main()
