import re
from pydantic import BaseModel, Field, SecretStr, field_validator

class UserCreate(BaseModel):
    FIRSTNAME: str = Field(..., description="Provide First Name")
    LASTNAME: str = Field(..., description="Provide Last Name")
    JOBTITLE: str = Field(..., description="Provide Job Title")
    DEPARTMENT: str = Field(..., description="Provide Department Name")
    MANAGER: str = Field(..., description="Provide manager Name")
    CITY: str = Field(..., description="Provide Location(City)")
    PASSWORD: SecretStr = Field(..., description="Provide the password")

    @field_validator("FIRSTNAME", "LASTNAME")
    @classmethod
    def sanitise_name(cls, value: str) -> str:
        # Allow only letters, spaces, hyphens, apostrophes (e.g. O'Brien, Mary-Jane)
        if not re.fullmatch(r"[A-Za-z\s\-']+", value):
            raise ValueError(
                "Name must contain only letters, spaces, hyphens, or apostrophes"
            )
        return value.strip()


class UserDetails(BaseModel):
    username: str
    Email: str

class UserResponse(BaseModel):
    message: str
    user_details: UserDetails



    # FirstName
    # LastName
    # Email
    # eid
    # JobTitle
    # Department
    # Company
    # Manager
    # City
    # State
    # Zipcode
    # Country
