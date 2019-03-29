# Weather Sign

##### Reusing an EL233 flip-digit display originally designed for measuring truck weights to display current weather conditions

## Usage

Obtain an [Accuweather API key](https://developer.accuweather.com/) and set the `ACCUWEATHER_API_KEY` environment variable accordingly.  Edit `main.py` to reference the appropriate dev for the serial interface to the EL233.


## Notes

Updates are scheduled every 30 minutes: the free Accuweather key is limited to 50 calls per day, and physically flipping the digits more often is distracting. 