from ldap3 import Server, Connection, ALL, SUBTREE
from config import get_ldap_url, get_bind_user, get_bind_user_pass

LDAP_URL = get_ldap_url()
BIND_USER = get_bind_user()
BIND_USER_PASS = get_bind_user_pass()

BASE_DN = "OU=accounts,DC=homelab,DC=local"

server = Server(LDAP_URL, get_info=ALL)
conn = Connection(server, user=BIND_USER, password=BIND_USER_PASS, auto_bind=True)

# --- SEARCH ---
# conn.search(search_base=BASE_DN,
#             search_filter="(cn=adinda)",
#             search_scope=SUBTREE,
#             attributes=["cn", "givenName", "sn", "mail", "objectSid"]
#         )

# if conn.entries:
#     user = conn.entries[0]

#     dn = user.entry_dn
#     ous = [
#         part.split("=", 1)[1]
#         for part in dn.split(",")
#         if part.upper().startswith("OU=")
#     ]
    
#     user_info = {
#         "cn": str(user.cn),
#         "full name": f"{str(user.givenName)} {str(user.sn)}",
#         "mail": str(user.mail),
#         "objectSid": str(user.objectSid),
#         "user location": ous[2]
#     }

#     print(user_info)
# else:
#     print("no user found")

#============
# OU Search

SEARCH_BASE = "DC=homelab,DC=local" 
search_filter = "(Name=Engineering)"
search_attributes = ["distinguishedName"]

conn.search(
    search_base=SEARCH_BASE,
    search_filter=search_filter,
    search_scope=SUBTREE,
    attributes=search_attributes,
)

if conn.entries:
    for entry in conn.entries:
        print(entry.entry_dn)
else:
    print("No AD object found matching 'Engineering'.")

# 6. Clean up connection
conn.unbind()


#============
# OU Creation
# ou_name = "Engineering"

# ou_dn = f"OU={ou_name},OU=Accounts,DC=homelab,DC=local"

# conn.add(
#     dn=ou_dn,
#     object_class=["top", "organizationalUnit"],
#     attributes={
#         "ou": ou_name
#     }
# )

# if conn.result["result"] == 0:
#     print("OU created successfully")
# else:
#     print("Failed to create OU")
#     print(conn.result)