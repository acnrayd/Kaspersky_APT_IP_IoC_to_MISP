# Converter and Pusher: Kaspersky APT IoC IP Data Feed to MISP (Unofficial)

## Kaspersky APT IoC IP Data Feed
Kaspersky Labs has a dedicated team for APT-Research called GReAT - GLobal Research and Analysis Team. GReAT team now tracks 100+ threat actors, uncovering the most sophisticated and dangerous targeted attacks, cyber-espionage campaigns, major malware, ransomware and underground cybercriminal trends in 85 countries. Kaspersky is also providing APT-related IoC's as-a-service for their enterprise customers. 

APT-IP-Data-Feeds are one of these Threat Data Feed services. APT-related Data Feeds only provided in non-standard JSON format, so ingesting these feeds to a threat intelligence platform requires some scripts to match target formats. 
 
## MISP (Malware Information Sharing Platform) 
MISP is a open source threat intelligence platform (TIP) to store and share related cyber-threat-intelligence, including threat indicators such as IP, URL and hashes, threat reports and similar threat-intel data. MISP also has an API for automated data ingestion & export.

## What is the purpose of this script?
KL APT Data Feeds are published in non-standard JSON format. However, MISP API only accepts data in specifically designed JSON. Ingesting these feeds to MISP requires scripts to convert and match MISP target format. After converting data to MISP-standard JSON, script pushes the feeds (including indicator, date and publication_name) by using Python Requests library as HTTP POST. While pushing the indicators into the MISP, script also tags all attributes and events with "kaspersky_apt_ioc_ip" tag. Also, script performs deduplication for repeated entries and merges related values under the same "publication_name" field.

Please keep in mind that it does not perform any checking on MISP side - so for every ingestion, you need to provide diff-feeds every time.

This is not an official release from Kaspersky and has no relationship with the company. Use it at your own risk and mind-the-bugs.

## How to use this script?
1) Put APT_IP_Data_Feed.json to the same folder with the script.
2) Create a pip-env with Python 2.7 and install "requests" package
3) Get the API token from: https://MISP_IP/events/automation 
4) Replace the "authorisation" API token with yours on main script, line 48
5) Replace MISP URL with your MISP instance URL, line 32
6) Run the script using python2.7.
7) Script will create new events for every new "publication_name" and push IP's as "attributes" under the related events.

## How does KL APT IOC feeds look like?
A example .json file is included in the repository.

## How does a MISP request look like?
For pushing data into MISP, you need several steps:

1- Create a MISP API token from: https://MISP_IP/events/automation

2- Use following headers for HTTP POST request:
    
    headers = {
        'authorization': "YOUR_API_TOKEN",
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }
    
3- For creating a new "event" in MISP, send a HTTP-POST to https://MISP_IP/events with required headers and following body (this is the minimum to create a new event)

    {
        "Event": 
        {
            "date": "2019-09-23",
            "info": "Test"
        }
    } 

This will create a new "event" in MISP, with the name "Test", assign a "id" to newly created object, and return all related details as a response including "id". An example for this response has been added as "MISP_response_example.json" If you need to add other details to the event, you can use the example as template.

4- After creating the event, if you need to add other details as attributes, you should create another request including the attributes and event "id". An example for a event with attributes and other details has been added to repository under the name of "MISP_request_with_attributes_example.json" After you create your requested event including attributes, you should send the HTTP POST request to: https://MISP_IP/events/YOUR_EVENT_ID. All fields will be updated according to your posted JSON. 

On the previous step I have created an event, in the response I have found that event "id" is "563". Now I am sending a HTTP-POST to https://MISP_IP/events/563 with previous headers and include following block as body. This action will add a "ip-src" attribute to event ID "563" and add related IP value (10.20.30.50) to the event.

    {
        "Attribute": [
            {
                "type": "ip-src",
                "category": "Network activity",
                "value": "10.20.30.50"
            }
        ]
    }

## Disclaimer
The software is developed by a independent author without any professional expectations and released as open-source. Project will not be maintained for security vulnerabilities and feature enhancements. This product has no affiliations with the designated vendors. All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Acknowledgement
Thanks to Reddit user r/Revofev92 for helping me to create deduplication / merging part of the script.
