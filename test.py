import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Patch LDAP at import time so main.py never attempts a real connection
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def mock_ldap_session():
    """Session-scoped patch: replaces ldap3.Server and ldap3.Connection
    before main.py is imported, preventing any real network call."""
    with patch("ldap3.Server") as mock_server, \
         patch("ldap3.Connection") as mock_conn_cls:

        mock_conn_cls.return_value = MagicMock()
        yield mock_server, mock_conn_cls


@pytest.fixture(scope="session")
def client(mock_ldap_session):
    # Import here so the ldap3 patch above is already active
    from main import app
    return TestClient(app)


@pytest.fixture
def ldap_conn(mock_ldap_session):
    """Return the shared mock Connection instance used inside main.py."""
    from main import conn
    return conn


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------
class TestHome:
    def test_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_welcome_message(self, client):
        data = client.get("/").json()
        assert data["message"] == "Welcome to Ldap API service"


# ---------------------------------------------------------------------------
# GET /users/{username}
# ---------------------------------------------------------------------------
class TestGetUser:
    def _make_entry(self, cn, given, sn, mail, sid, dn):
        entry = MagicMock()
        entry.cn = cn
        entry.givenName = given
        entry.sn = sn
        entry.mail = mail
        entry.objectSid = sid
        entry.entry_dn = dn
        return entry

    def test_user_found_returns_200(self, client, ldap_conn):
        dn = "CN=adinda,OU=Engineering,OU=IT,OU=accounts,DC=homelab,DC=local"
        ldap_conn.entries = [
            self._make_entry("adinda", "Adinda", "Putri", "adinda@homelab.local", "S-1-5-21-1", dn)
        ]

        response = client.get("/users/adinda")
        assert response.status_code == 200

    def test_user_found_response_body(self, client, ldap_conn):
        dn = "CN=adinda,OU=Engineering,OU=IT,OU=accounts,DC=homelab,DC=local"
        ldap_conn.entries = [
            self._make_entry("adinda", "Adinda", "Putri", "adinda@homelab.local", "S-1-5-21-1", dn)
        ]

        data = client.get("/users/adinda").json()
        assert data["message"] == "user details found for adinda"
        info = data["user info"]
        assert info["cn"] == "adinda"
        assert info["full name"] == "Adinda Putri"
        assert info["mail"] == "adinda@homelab.local"
        assert info["objectSid"] == "S-1-5-21-1"
        assert info["user location"] == "Engineering"

    def test_user_not_found_returns_404(self, client, ldap_conn):
        ldap_conn.entries = []
        response = client.get("/users/ghost")
        assert response.status_code == 404

    def test_user_not_found_detail(self, client, ldap_conn):
        ldap_conn.entries = []
        data = client.get("/users/ghost").json()
        assert "ghost" in data["detail"]


# ---------------------------------------------------------------------------
# POST /users
# ---------------------------------------------------------------------------
class TestCreateUser:
    def test_create_user_returns_200(self, client):
        response = client.post("/users")
        assert response.status_code == 200

    def test_create_user_message(self, client):
        data = client.post("/users").json()
        assert "created" in data["message"].lower()


# ---------------------------------------------------------------------------
# GET /organizational_unit/{ouName}
# ---------------------------------------------------------------------------
class TestGetOU:
    def _make_ou_entry(self, dn):
        entry = MagicMock()
        entry.entry_dn = dn
        return entry

    def test_ou_found_returns_200(self, client, ldap_conn):
        ldap_conn.entries = [
            self._make_ou_entry("OU=Engineering,OU=accounts,DC=homelab,DC=local")
        ]
        response = client.get("/organizational_unit/Engineering")
        assert response.status_code == 200

    def test_ou_found_response_body(self, client, ldap_conn):
        expected_dn = "OU=Engineering,OU=accounts,DC=homelab,DC=local"
        ldap_conn.entries = [self._make_ou_entry(expected_dn)]

        data = client.get("/organizational_unit/Engineering").json()
        assert data["OU Tree"] == expected_dn

    def test_ou_not_found_returns_404(self, client, ldap_conn):
        ldap_conn.entries = []
        response = client.get("/organizational_unit/NonExistent")
        assert response.status_code == 404

    def test_ou_not_found_detail(self, client, ldap_conn):
        ldap_conn.entries = []
        data = client.get("/organizational_unit/NonExistent").json()
        assert "NonExistent" in data["detail"]


# ---------------------------------------------------------------------------
# POST /organizational_unit
# ---------------------------------------------------------------------------
class TestCreateOU:
    def test_create_ou_success_returns_200(self, client, ldap_conn):
        ldap_conn.result = {"result": 0, "description": "success"}
        response = client.post(
            "/organizational_unit",
            params={"new_ou_name": "Finance", "top_ou": "OU=accounts,DC=homelab,DC=local"}
        )
        assert response.status_code == 200

    def test_create_ou_success_response_body(self, client, ldap_conn):
        ldap_conn.result = {"result": 0, "description": "success"}
        data = client.post(
            "/organizational_unit",
            params={"new_ou_name": "Finance", "top_ou": "OU=accounts,DC=homelab,DC=local"}
        ).json()
        assert "created" in data["message"].lower()
        assert data["OU Details"] == "OU=Finance,OU=accounts,DC=homelab,DC=local"

    def test_create_ou_ldap_failure_returns_500(self, client, ldap_conn):
        ldap_conn.result = {"result": 68, "description": "entryAlreadyExists"}
        response = client.post(
            "/organizational_unit",
            params={"new_ou_name": "Finance", "top_ou": "OU=accounts,DC=homelab,DC=local"}
        )
        assert response.status_code == 500

    def test_create_ou_ldap_failure_detail(self, client, ldap_conn):
        ldap_conn.result = {"result": 68, "description": "entryAlreadyExists"}
        data = client.post(
            "/organizational_unit",
            params={"new_ou_name": "Finance", "top_ou": "OU=accounts,DC=homelab,DC=local"}
        ).json()
        assert "Failed" in data["detail"]
