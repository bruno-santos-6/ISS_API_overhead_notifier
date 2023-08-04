import time
from requests import get
from datetime import datetime
from smtplib import SMTP
import schedule

MY_EMAIL = "brunocool719@gmail.com"
MY_KEY = "nbloqgodrucgiuig"
MY_LAT = -23.179140
MY_LONG = -45.887241


def is_iss_overhead():
    response_iss = get(url="https://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = data_iss["iss_position"]["latitude"]
    iss_longitude = data_iss["iss_position"]["longitude"]

    # Your position is within +5 or -5 degrees of the iss position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = get(url="http://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour


def notify():
    if is_iss_overhead() and time_now > sunset:
        if time_now < sunrise:
            my_subject = "Look Up! ☝️"
            my_message = "The ISS is above you in the sky."
            with SMTP(host="smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_KEY)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"{my_subject}\n\n{my_message}"
                )


schedule.every(60).seconds.do(notify)
while True:
    schedule.run_pending()
    time.sleep(1)
