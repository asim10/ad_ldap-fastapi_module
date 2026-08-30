from ldap3 import Server, Connection, ALL, Tls
import ssl
from config import get_ldap_url, get_bind_user, get_bind_user_pass

LDAP_URL = get_ldap_url()
BIND_USER = get_bind_user()
BIND_USER_PASS = get_bind_user_pass()

tls = Tls(validate=ssl.CERT_NONE)
server = Server(LDAP_URL, get_info=ALL, use_ssl=True, tls=tls)
conn = Connection(server, user=BIND_USER, password=BIND_USER_PASS, auto_bind=True)
