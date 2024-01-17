import requests

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

# how do we want to get accesstoken?

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