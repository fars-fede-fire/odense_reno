# Odense Renovation

Home Assistant custom component for getting trash and recycle pickup dates from Odense Renovation

Available as custom repository in HACS

Heavily based on https://github.com/home-assistant/core/tree/dev/homeassistant/components/twentemilieu by @frenck

## Setup
### 1)
Go to https://mit.odenserenovation.dk/hentkalender
Type and find your address
![find addressNo](https://github.com/fars-fede-fire/odense_reno/blob/main/photos/get_api_1.PNG)

### 2)
Copy addressNo (numbers only) from the URL
![copy addressNo from url](https://github.com/fars-fede-fire/odense_reno/blob/main/photos/get_api_2.png)

### 3)
Insert when asked for in integration setup
![setup integration](https://github.com/fars-fede-fire/odense_reno/blob/main/photos/integration_setup.PNG)

### 4)
Sensors equal to your bins is now available with date for next planned pickup
![dashboard with sensor](https://github.com/fars-fede-fire/odense_reno/blob/main/photos/dashboard.PNG)

### TODO:
See examples for template sensors