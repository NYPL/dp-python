import requests
from pathlib import Path
import time
import logging
import xml.etree.ElementTree as ET

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

# def request_api_call(type: str, accesstoken: str, url: str) -> requests.Response:
#     headers






'''
curl -X 'POST' \
  'https://nypl.preservica.com/api/entity/structural-objects/d8ba26ae-e915-4071-8d27-4838ee73f0d7/exports' \
  -H 'accept: text/plain;charset=UTF-8' \
  -H 'Content-Type: application/xml;charset=UTF-8' \
  -d '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ExportAction xmlns="http://preservica.com/EntityAPI/v6.12" xmlns:xip="http://preservica.com/XIP/v6.12">
    <IncludeContent>Content</IncludeContent>
    <IncludeMetadata>Metadata</IncludeMetadata>
    <IncludedGenerations>All</IncludedGenerations>
    <IncludeParentHierarchy>false</IncludeParentHierarchy>
</ExportAction>'

'''

"""
1. POST
https://nypl.preservica.com/api/entity/structural-objects/d8ba26ae-e915-4071-8d27-4838ee73f0d7/exports
header needs to include XML
This returns a progress token

2. Check status
https://nypl.preservica.com/api/entity/progress/8ba8b96d-a60c-466d-9bd5-73ae7ea7325e?includeErrors=true

3. GET
https://nypl.preservica.com/api/entity/actions/exports/8ba8b96d-a60c-466d-9bd5-73ae7ea7325e/content
"""

def main():
    """
    generate token
    API
    """
    user = input("Enter user name: ")
    pw = input("Enter password: ")
    tenant = input("Enter tenant (nypl or nypltest)")

    credential_set = (user, pw, tenant)

    accesstoken = get_token(credential_set)

    export_so_url = "https://nypl.preservica.com/api/entity/structural-objects/85fa0068-f63b-49fc-8310-e0e11944c45a/exports"
    export_headers = {
        "Preservica-Access-Token": accesstoken
    }
    xml_str = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ExportAction xmlns="http://preservica.com/EntityAPI/v6.12" xmlns:xip="http://preservica.com/XIP/v6.12">
    <IncludeContent>Content</IncludeContent>
    <IncludeMetadata>Metadata</IncludeMetadata>
    <IncludedGenerations>All</IncludedGenerations>
    <IncludeParentHierarchy>false</IncludeParentHierarchy>
    </ExportAction>"""
    xml_data = ET.fromstring(xml_str)
    post_response = requests.request("POST", export_so_url, headers=export_headers, data=xml_data.text)
    print(post_response)



if __name__ == "__main__":
    main()