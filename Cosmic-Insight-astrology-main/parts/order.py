import random
import requests

def genrate_otp():
    return random.randint(100000,999999)

def send_sms(mobile,otp):
    url =  f"https://2factor.in/API/V1/API_KEY/SMS/{mobile}/{otp}/OTP1"
    requests.get(url)
