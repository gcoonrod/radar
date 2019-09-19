# radar
Display flight tracks on the UnicornHatHD module for Raspberry Pi.

![](SmartSelect_20190110-110709_Video%20Player.gif)

This will run without the UnicornHatHD module, but will simply print information to the console.

## Prerequisites 
* Dependencies: numpy, requests, dotenv, and UnicornHatHD and associated python module.
* ADSBExchange API Key: [ADSBExchange API](https://www.adsbexchange.com/data/)
* Python3

## Setup
1. Create a `.env` file that looks like:
    ```.env
    API_KEY=YOUR_ADSBX_KEY
    DEBUG=0
    LOG_ENABLE=0
    ```
2. Create a `config.json` file and update it to match your area of interest:
    * `cp config.json.example config.json`

3. Run the tracker.py module. This will load data from config.json, which by default is configured to the area around London Heathrow. Alternative coordinates for the map, tracking range, and any fixed points you wish to display can be specified in config.json. I will include some alternative config files as examples (see for now config_ire.json which is the whole of Ireland).
4. If you don't have the UnicornhatHD or you'd like to debug an issue and need to see console output change `DEBUG=1` and `LOG_ENABLE=1` in your `.env` file.
## Acknowledgments
The Kalman Filter code is not currently used but is included in the module for future reference and in case anyone wants to get it working properly. The present code is adapted from the examples at http://scottlobdell.me/2014/08/kalman-filtering-python-reading-sensor-input/
