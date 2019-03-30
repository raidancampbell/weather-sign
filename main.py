import json
import os
import requests
import time
from apscheduler.schedulers.background import BlockingScheduler
from EL233 import EL233


class WeatherSign:
    def __init__(self, accuweather_api_key, EL233_dev):
        self.sign = EL233(EL233_dev)
        self.request_params = {
            "apikey": accuweather_api_key,
            "details": "true"
        }
        self.scheduler = None

    request_url = "http://dataservice.accuweather.com/currentconditions/v1/5622_POI"
    base_url = "http://dataservice.accuweather.com/currentconditions/v1/5622_POI"

    def update(self):
        response = requests.get(WeatherSign.base_url, params=self.request_params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
        d = json.loads(response.content)
        _time = d[0]['LocalObservationDateTime']
        deg_f = round(d[0]['Temperature']['Imperial']['Value'])
        rh = round(d[0]['RelativeHumidity'])
        print(f'{_time} temp: {deg_f}, humidity: {rh}')
        self.sign.display_temp_and_humidity(temp=deg_f, humidity=rh)
        time.sleep(30 * 60)

    def update_forever(self):
        if self.scheduler and self.scheduler.running:
            return
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(WeatherSign.update, trigger='cron', minute="0,18", max_instances=1,
                               coalesce=True, args=[self])
        self.scheduler.start()


if __name__ == '__main__':
    weather_sign = WeatherSign(os.environ['ACCUWEATHER_API_KEY'], '/dev/tty.usbserial-AE01IQ4F')
    weather_sign.update_forever()
