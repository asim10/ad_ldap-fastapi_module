import os
from dotenv import load_dotenv

load_dotenv()

def get_ldap_url():
    LDAP_URL = os.getenv("LDAP_HOST_URL")
    return LDAP_URL

def get_bind_user():
    BIND_USER = os.getenv("LDAP_BIND_USER")
    return BIND_USER

def get_bind_user_pass():
    BIND_USER_PASS = os.getenv("LDAP_BIND_USER_PASS")
    return BIND_USER_PASS