from fastapi import FastAPI, HTTPException, status
from ldap3 import Server, Connection, ALL, SUBTREE
from config import get_ldap_url, get_bind_user, get_bind_user_pass, get_user_ou, get_state, get_zipcode
from humanUserBase import UserCreate, UserResponse
from models import get_user_dn

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
@app.post("/users", response_model = UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    firstname = user_in.FIRSTNAME
    lastname = user_in.LASTNAME
    job_title = user_in.JOBTITLE
    department = user_in.DEPARTMENT
    manager_username = user_in.MANAGER
    city = user_in.CITY
    password = user_in.PASSWORD

    email = f"{firstname}.{lastname}@homelab.local"
    username = f"{firstname[0].lower()}{lastname.lower()}"
    display_name = f"{firstname} {lastname}"

    target_ou = f"OU=Associates,OU=User Accounts,OU={get_user_ou(city)},OU=Accounts,DC=homelab,DC=local"

    state = get_state(city)
    zipcode = get_zipcode(city)
    country = "India"
    company = "Homelab"

    manager_dn = get_user_dn(manager_username)

    user_dn = f"CN={username},{target_ou}"

    attributes = {
        "cn": username,
        "givenName": firstname,
        "sn": lastname,
        "displayName": display_name,
        "mail": email,
        "title": job_title,
        "department": department,
        "company": company,
        "manager": manager_dn,
        "l": city,
        "st": state,
        "postalCode": zipcode,
        "co": country,
        "userPrincipalName": f"{username}@homelab.local",
        "sAMAccountName": username
    }

    conn.add(
        dn=user_dn,
        object_class=[
            "top",
            "person",
            "organizationalPerson",
            "user"
        ],
        attributes=attributes
    )

    if conn.result["result"] != 0:
        raise HTTPException (
            status_code = 500,
            detail = f"Failed to create user. {conn.result}"
        )
    
    return {
        "message": "User Created sucessfully",
        "user_details": {
            "username": username,
            "Email": email
        }
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

@app.post("/organizational_unit")
def create_ou(new_ou_name: str, top_ou: str):
    OU_DN = f"OU={new_ou_name},{top_ou}"
    
    # DEBUG PRINT: Check terminal logs when calling curl
    print(f"DEBUG: Constructing LDAP DN -> '{OU_DN}'")

    conn.add(
        dn=OU_DN,
        object_class=["top", "organizationalUnit"],
        attributes={
            "ou": new_ou_name
        }
    )

    if conn.result["result"] != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create OU at '{OU_DN}'. LDAP Error: {conn.result}"
        )

    return {
        "message": "OU Created successfully",
        "OU Details": OU_DN
    }