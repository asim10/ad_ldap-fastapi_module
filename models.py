from ldap3 import SUBTREE
from ldap_connection import conn

def get_user_dn(username: str):
    """Get user AD DN Details"""
    BASE_DN = "OU=accounts,DC=homelab,DC=local"
    conn.search(search_base=BASE_DN,
                search_filter=f"(cn={username})",
                search_scope=SUBTREE,
                attributes=["cn", "givenName", "sn", "mail", "objectSid"]
            )

    if not conn.entries:
        return None

    return conn.entries[0].entry_dn



if __name__ == "__main__":
    username = input("Enter Username: ")
    print(get_user_dn(username))