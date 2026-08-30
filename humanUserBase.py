from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    FIRSTNAME: str = Field(..., description = "Provide First Name")
    LASTNAME: str = Field(..., description = "Provide Last Name")
    JOBTITLE: str = Field(..., description = "Provide Job Title")
    DEPARTMENT: str = Field(..., description = "Provide Department Name")
    MANAGER: str = Field(..., description = "Provide manager Name")
    CITY: str = Field(..., description = "Provide Location(City)")
    PASSWORD: str = Field(..., description = "Provide the password")

class UserResponse(BaseModel):
    username: str
    email: EmailStr


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
