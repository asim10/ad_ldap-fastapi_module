import os
from dotenv import load_dotenv

load_dotenv()

OU = {
    "pune": "PUNOFFICE",
    "chennai": "CHNOFFICE",
    "hyderabad": "HYDOFFICE",
    "kolkata": "KOLOFFICE"
}

STATE = {
    "pune": "MH",
    "chennai": "TN",
    "hyderabad": "TG",
    "kolkata": "WB"
}

ZIPCODE = {
    "pune": 412207,
    "chennai": 600089,
    "hyderabad": 501510,
    "kolkata": 700010
}

def get_ldap_url():
    LDAP_URL = os.getenv("LDAP_HOST_URL")
    return LDAP_URL

def get_bind_user():
    BIND_USER = os.getenv("LDAP_BIND_USER")
    return BIND_USER

def get_bind_user_pass():
    BIND_USER_PASS = os.getenv("LDAP_BIND_USER_PASS")
    return BIND_USER_PASS

def get_user_ou(city: str):
    """Method to get respective AD-OU based on City"""
    OU_KEYWORD = OU.get(city)
    return OU_KEYWORD

def get_state(city: str):
    """Method to get respective State based on City"""
    CITY_STATE = STATE.get(city)
    return CITY_STATE

def get_zipcode(city: str):
    """Method to respective zipcode based on the location"""
    CITY_ZIPCODE = ZIPCODE.get(city)