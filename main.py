from fastapi import FastAPI, HTTPException
from ldap3 import Server, Connection, ALL, SUBTREE
from config import get_ldap_url, get_bind_user, get_bind_user_pass

app = FastAPI()

LDAP_URL = get_ldap_url()
BIND_USER = get_bind_user()
BIND_USER_PASS = get_bind_user_pass()

server = Server(LDAP_URL, get_info=ALL)
conn = Connection(server, user=BIND_USER, password=BIND_USER_PASS, auto_bind=True)

# Home
@app.get("/")
def home():
    return {
        "message": "Welcome to Ldap API service"
    }

# Find User details
@app.get("/users/{username}")
def get_user(username: str):
    BASE_DN = "OU=accounts,DC=homelab,DC=local"
    # --- SEARCH ---
    conn.search(search_base=BASE_DN,
                search_filter=f"(cn={username})",
                search_scope=SUBTREE,
                attributes=["cn", "givenName", "sn", "mail", "objectSid"]
            )
    
    if not conn.entries:
        raise HTTPException(
            status_code = 404,
            detail = f"no user found for cn={username}"
        )
    
    user = conn.entries[0]
    dn = user.entry_dn
    ous = [
        part.split("=", 1)[1]
        for part in dn.split(",")
        if part.upper().startswith("OU=")
    ]
    return {
        "message": f"user details found for {username}",
        "user info": {
            "cn": str(user.cn),
            "full name": f"{str(user.givenName)} {str(user.sn)}",
            "mail": str(user.mail),
            "objectSid": str(user.objectSid),
            "user location": ous[2]
        }
    }

# Create User
@app.post("/users")
def create_user():
    return {
        "message": "User Created sucessfully"
    }

# Find Organizational Unit
@app.get("/organizational_unit/{ouName}")
def get_ou(ouName: str):
    SEARCH_BASE = "DC=homelab,DC=local" 
    search_filter = f"(Name={ouName})"
    search_attributes = ["distinguishedName"]

    conn.search(
        search_base=SEARCH_BASE,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=search_attributes,
    )

    if not conn.entries:
        raise HTTPException(
            status_code = 404,
            detail = f"No AD object found matching '{ouName}'."
        )

    entry = conn.entries[0]

    return {
        "OU Tree": entry.entry_dn
    }

# Create Organizational Unit
@app.post("/organizational_unit")
def create_ou(new_ou_name: str, top_ou: str):
    OU_DN = f"OU={new_ou_name},{top_ou}"

    conn.add(
        dn=OU_DN,
        object_class=["top", "organizationalUnit"],
        attributes={
            "ou": new_ou_name
        }
    )

    if conn.result["result"] != 0:
        raise HTTPException(
            status_code = 500,
            detail = f"Failed to create OU. {conn.result}"
        )

    return {
        "message": "OU Created successfully",
        "OU Details": OU_DN
    }