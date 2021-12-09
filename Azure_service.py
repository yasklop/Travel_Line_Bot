
'''
 Azure translate

'''
import requests, uuid, json

def translate_to(text, to_language):

    subscription_key = "175a7f430fdd47c0a1aeb100baeb5c71"
    endpoint = "https://api.cognitive.microsofttranslator.com/"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "southcentralus"


    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': [to_language]
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    for i in response:
        return (i['translations'][0]['text'])

'''
 End Azure translate

'''

'''
 Azure language

'''
# handle text
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


key = "7efb6a87241d4df3be274cbeb3f86efa"
endpoint = "https://linbotlanguage.cognitiveservices.azure.com/"

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting the language of text
def language_detection_example(client, text):
    try:
        documents = [text]
        response = client.detect_language(documents = documents, country_hint = 'us')[0]
        #print("Language: ", response.primary_language.name)
        
        return "Language: " + response.primary_language.name

    except Exception as err:
        print("Encountered exception. {}".format(err))

'''
 End Azure language

'''

'''
 Azure OCR

'''
# handle msg
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


subscription_key = "ca07131a12a84163bdcadb8d151d5be0"
endpoint = "https://ohohoh.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


#text_current = ""
def text_img(img_line):
    print("===== Read File - local =====")
    # Get image path
    read_image_path = img_line
    # Open the image
    read_image = open(read_image_path, "rb")

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...')
        time.sleep(10)

    # Print results, line by line
   # total = ""
    if read_result.status == OperationStatusCodes.succeeded:
        total = ""
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                #text_language = language_detection_example(client, line.text)
                #result_text = line.text + "\n" + text_language + "\n"
                if total is "":
                    total += line.text
                else:
                    total += "\n" + line.text 
               # print(line.text)
                #print(line.bounding_box)

    return total
'''
END - Read File - local

'''

