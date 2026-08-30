from ldap3 import Server, Connection, SIMPLE, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError

LDAP_SERVER   = "ldap://ldapvip.homelab.local:389"
LDAP_BASE_DN  = "DC=homelab,DC=local"

# Service account used only to search for the user's DN
BIND_USER_DN  = "cn=dev9bind,OU=Service Accounts,OU=Resources,DC=homelab,DC=local"
BIND_PASSWORD = "P9Kx30J7noP3ti6N"


def find_user_dn(username: str) -> str | None:
    """
    Binds with a service account and searches for the user's full DN
    across all OUs under the base DN.
    """
    server = Server(LDAP_SERVER, get_info=ALL)

    try:
        conn = Connection(
            server,
            user=BIND_USER_DN,
            password=BIND_PASSWORD,
            authentication=SIMPLE,
            auto_bind=True,
        )

        conn.search(
            search_base=LDAP_BASE_DN,
            search_filter=f"(sAMAccountName={username})",
            search_scope=SUBTREE,
            attributes=["distinguishedName"],
        )

        if not conn.entries:
            print(f"User '{username}' not found in directory.")
            return None

        user_dn = conn.entries[0].distinguishedName.value
        conn.unbind()
        return user_dn

    except LDAPException as e:
        print(f"LDAP search error: {e}")
        return None


def authenticate_ldap(username: str, password: str) -> bool:
    """
    Finds the user's DN across all OUs then authenticates with their password.
    """
    user_dn = find_user_dn(username)
    if not user_dn:
        return False

    server = Server(LDAP_SERVER, get_info=ALL)

    try:
        conn = Connection(
            server,
            user=user_dn,
            password=password,
            authentication=SIMPLE,
            auto_bind=True,
        )
        print(f"Authentication successful for: {username}")
        conn.unbind()
        return True

    except LDAPBindError:
        print("Authentication failed: Invalid credentials.")
        return False
    except LDAPException as e:
        print(f"LDAP connection error: {e}")
        return False

# def authenticate_ldap_upn(username: str, password: str, domain: str = "homelab.local") -> bool:
#     """
#     Authenticates directly using UPN (user@domain) — no service account needed.
#     AD accepts UPN format without requiring a prior DN lookup.
#     """
#     upn = f"{username}@{domain}"
#     server = Server(LDAP_SERVER, get_info=ALL)

#     try:
#         conn = Connection(
#             server,
#             user=upn,
#             password=password,
#             authentication=SIMPLE,
#             auto_bind=True,
#         )
#         print(f"Authentication successful for: {upn}")
#         conn.unbind()
#         return True

#     except LDAPBindError:
#         print("Authentication failed: Invalid credentials.")
#         return False
#     except LDAPException as e:
#         print(f"LDAP connection error: {e}")
#         return False



if __name__ == "__main__":
    user_name = input("Enter username: ")
    user_pwd  = input("Enter password: ")

    # is_authenticated = authenticate_ldap_upn(user_name, user_pwd)
    is_authenticated = authenticate_ldap(user_name, user_pwd)
    print(f"Authenticated: {is_authenticated}")
