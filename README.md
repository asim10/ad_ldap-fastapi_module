<div align="center">

<img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Active%20Directory-0078D4?style=for-the-badge&logo=microsoft&logoColor=white" alt="Active Directory"/>
<img src="https://img.shields.io/badge/LDAP-FF6B35?style=for-the-badge&logo=ldap&logoColor=white" alt="LDAP"/>

# AD LDAP API

**A lightweight REST API for managing Active Directory resources over LDAP.**

</div>

---

## � Table of Contents

- [📖 Overview](#-overview)
- [🔧 Prerequisites](#-prerequisites)
- [🚀 Getting Started](#-getting-started)
- [▶️ Running the API](#️-running-the-api)
- [📡 API Reference](#-api-reference)
  - [🏠 Health Check](#-health-check)
  - [👤 Users](#-users)
    - [Get User Details](#get-user-details)
    - [Create User](#create-user)
  - [🗂️ Organizational Units](#️-organizational-units)
    - [Find an OU](#find-an-ou)
    - [Create an OU](#create-an-ou)
- [📁 Project Structure](#-project-structure)
- [📦 Dependencies](#-dependencies)

---

## �📖 Overview

This service wraps LDAP3 operations behind a clean FastAPI interface, enabling programmatic access to Active Directory for user lookups, OU discovery, and directory object creation — without needing direct AD tooling.

---

## 🔧 Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.8+ |
| Active Directory / LDAP Server | Accessible from host |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd ad_ldap-api_module
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
LDAP_HOST_URL=ldap://your-ad-server
LDAP_BIND_USER=binduser@domain
LDAP_BIND_USER_PASS=your-secure-password
```

| Variable | Description |
|---|---|
| `LDAP_HOST_URL` | LDAP server URL (e.g. `ldap://192.168.1.10`) |
| `LDAP_BIND_USER` | Distinguished Name of the bind/service account (e.g. `binduser@homelab.local`) |
| `LDAP_BIND_USER_PASS` | Password for the bind account |

> **🔒 Security note:** Never commit `.env` to version control. It is listed in `.gitignore`.

---

## ▶️ Running the API

**Local only**
```bash
uvicorn main:app --reload
```

**🌐 Remote access** — binds to all interfaces on port `8088`, accessible from other machines on the network:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8088
```

| Interface | Local | Remote |
|---|---|---|
| API Base | `http://127.0.0.1:8000` | `http://<host-ip>:8088` |
| Interactive Docs (Swagger) | `http://127.0.0.1:8000/docs` | `http://<host-ip>:8088/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` | `http://<host-ip>:8088/redoc` |

> **⚠️ Note:** Ensure port `8088` is open in your firewall rules before exposing the API remotely.

---

## 📡 API Reference

### 🏠 Health Check

```
GET /
```

Returns a welcome message confirming the service is running.

---

### 👤 Users

#### Get User Details

```
GET /users/{username}
```

Looks up a user by Common Name (CN) within `OU=accounts,DC=homelab,DC=local`.

**Path Parameters**

| Parameter | Type | Description |
|---|---|---|
| `username` | string | The CN of the user to look up |

**Response `200 OK`**
```json
{
  "message": "user details found for john",
  "user info": {
    "cn": "john",
    "full name": "John Doe",
    "mail": "john@homelab.local",
    "objectSid": "S-1-5-21-...",
    "user location": "Engineering"
  }
}
```

**Response `404 Not Found`**
```json
{
  "detail": "no user found for cn=john"
}
```

---

#### Create User

```
POST /users
```

> Creates a new user entry in Active Directory.

---

### 🗂️ Organizational Units

#### Find an OU

```
GET /organizational_unit/{ouName}
```

Returns the full Distinguished Name (DN) of a matching Organizational Unit.

**Path Parameters**

| Parameter | Type | Description |
|---|---|---|
| `ouName` | string | Name of the OU to locate |

**Response `200 OK`**
```json
{
  "OU Tree": "OU=Engineering,OU=Accounts,DC=homelab,DC=local"
}
```

**Response `404 Not Found`**
```json
{
  "detail": "No AD object found matching 'Engineering'."
}
```

---

#### Create an OU

```
POST /organizational_unit
```

Creates a new Organizational Unit nested under an existing one.

**Query Parameters**

| Parameter | Type | Description |
|---|---|---|
| `new_ou_name` | string | Name of the new OU |
| `top_ou` | string | Parent DN (e.g. `OU=Accounts,DC=homelab,DC=local`) |

**Response `200 OK`**
```json
{
  "message": "OU Created successfully",
  "OU Details": "OU=Engineering,OU=Accounts,DC=homelab,DC=local"
}
```

**Response `500 Internal Server Error`**
```json
{
  "detail": "Failed to create OU. {conn.result}"
}
```

---

## 📁 Project Structure

```
ad_ldap-api_module/
├── main.py             # FastAPI app — route definitions and LDAP logic
├── config.py           # Environment variable loader via python-dotenv
├── test.py             # Manual LDAP scratch scripts for development
├── requirements.txt    # Python dependencies
├── .env                # Local environment config (not committed)
└── .gitignore
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework and API routing |
| `uvicorn` | ASGI server |
| `ldap3` | LDAP client for Active Directory communication |
| `python-dotenv` | `.env` file loader |
