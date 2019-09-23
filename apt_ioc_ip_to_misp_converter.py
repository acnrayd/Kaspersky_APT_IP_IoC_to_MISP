import json
import requests # Do not forget to install requests package
import datetime
import random

apt_ioc_ip_oku = open("APT_IP_Data_Feed.json", "r")
apt_ioc_ip_json = json.load(apt_ioc_ip_oku)

##### dedupping and merging duplicate names and ip's - thanks to /u/Revofev92!

unique_names = set(json_item['publication_name'] for json_item in apt_ioc_ip_json)
output_json = []
for unique_name in unique_names:
    all_entries = [json_item for json_item in apt_ioc_ip_json if json_item['publication_name'] == unique_name]
    output_item = all_entries[0]
    if len(json_item) > 1:
        for duplicate_item in all_entries[1:]:
            output_item['ip'] += ", "
            output_item['ip'] += duplicate_item['ip']
    output_json.append(output_item)
    global json_dedup
    json_dedup = output_json

##### request to create events in MISP, getting event ID for further use. Replacing event info field as "publication name" and date to MISP-date format.

for pub_name_alim in output_json:
    #print(pub_name_alim["publication_name"])
    #print(publication_name["detection_date"])
    pub_name_converted = (pub_name_alim["publication_name"])
    date_converted = (pub_name_alim)["detection_date"]
    #print(pub_name_converted)
    url = "https://192.168.2.174/events/"
    payload = "{\n    \"Event\": {\n        \"info\": \"Caner Otomasyon442\",\n        \"date\": \"2019-09-20\",\n        \"Tag\": [\n                    {\n                        \"name\": \"kaspersky_apt_ioc_ip\"\n                    }\n                ]\n            }\n}\n"
    payload_conv = json.loads(payload)
    #print(payload_convv)
    payload_conv["Event"]["info"] = pub_name_converted
    date_converted2 = date_converted[:-6] # MISP does not accept time under "date" variable, so we need to delete last 6 chars.
    date_converted3 = date_converted2.replace(".","-") # MISP requires "-" to be used instead of "." in "date" variable.
    date_converted4 = datetime.datetime.strptime(date_converted3, "%d-%m-%Y") # Converting from DD-MM-YYYY to YYYY-MM-DD
    date_converted5 = str(date_converted4) # Converting date to string
    # Date_converted5 example output: "2019-09-16 00:00:00"
    date_converted6 = date_converted5[:-9] # Deleting last 9 char.
    payload_conv["Event"]["date"] = date_converted6
    payload_conv_json = json.dumps(payload_conv)
    #print(payload_conv_json)

    headers = {
        'authorization': "lCRV34i1zPRryyrlAQSh0dWKZsI9VlTU2TPqquYN",
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload_conv_json, headers=headers, verify=False)
    geteventid = json.loads(response.text) # getting event id
    geteventid2 = geteventid["Event"]["id"]
    geteventname = geteventid["Event"]["info"]
    #print(geteventid2)

    ##### Splitting IP's from comma seperated values to match JSON format

    ip = (pub_name_alim["ip"])
    ip_comma = ip.split(",")
    #print(ip_comma)
    vv = list(ip_comma)
    #print(vv[1)

    ##### Creating requests for each IP under related events
    for ip_add_seperated in vv:
        #print(ip_add_seperated)

        requesturl2 = url + geteventid2
        #print(requesturl2)

        payload2 = "\n{\n    \"Event\": {\n        \"Attribute\": [\n            {\n                \"type\": \"ip-src\",\n                \"category\": \"Network activity\",\n                \"value\": \"192.168.2.30\",\n                \"Tag\": [\n                    {\n                        \"id\": \"1\",\n                        \"name\": \"kaspersky_apt_ioc_ip\",\n                        \"colour\": \"#000000\",\n                        \"exportable\": true,\n                        \"user_id\": \"0\",\n                        \"hide_tag\": false,\n                        \"numerical_value\": null\n                    }\n                ]\n            }\n        ]\n    }\n}\n\n"
        payload2_conv = json.loads(payload2)
        payload2_conv["Event"]["Attribute"][0]["value"] = ip_add_seperated
        #print(ip_src)
        #payload2_conv["Event"]["Attribute"][value] = ip_src
        payload3 = json.dumps(payload2_conv)

        response = requests.request("POST", requesturl2, data=payload3, headers=headers, verify=False)
        print(response.text)
