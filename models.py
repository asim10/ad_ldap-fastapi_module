from ldap3 import Server, Connection, ALL, SUBTREE
from config import get_ldap_url, get_bind_user, get_bind_user_pass

LDAP_URL = get_ldap_url()
BIND_USER = get_bind_user()
BIND_USER_PASS = get_bind_user_pass()

server = Server(LDAP_URL, get_info=ALL)
conn = Connection(server, user=BIND_USER, password=BIND_USER_PASS, auto_bind=True)

def get_user_dn(username: str):
    """Get user AD DN Details"""
    BASE_DN = "OU=accounts,DC=homelab,DC=local"
    # --- SEARCH ---
    conn.search(search_base=BASE_DN,
                search_filter=f"(cn={username})",
                search_scope=SUBTREE,
                attributes=["cn", "givenName", "sn", "mail", "objectSid"]
            )
    user = conn.entries[0]
    dn = user.entry_dn

    return dn

if __name__ == "__main__":
    username = input("Enter Username: ")
    print(get_user_dn(username))