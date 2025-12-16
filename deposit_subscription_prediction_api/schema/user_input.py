
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Literal


class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the client")]
    job: Annotated[
        Literal[
            "admin", "technician", "services", "management", "retired",
            "student", "blue-collar", "entrepreneur", "self-employed",
            "unemployed", "housemaid", "unknown"
        ],
        Field(..., description="Type of job the client has")
    ]
    marital: Annotated[
        Literal["single", "married", "divorced"],
        Field(..., description="Marital status")
    ]
    education: Annotated[
        Literal["primary", "secondary", "tertiary", "unknown"],
        Field(..., description="Education level")
    ]
    default: Annotated[
        Literal["yes", "no"],
        Field(..., description="Has credit default?")
    ]
    balance: Annotated[int, Field(..., description="Account balance")]
    housing: Annotated[
        Literal["yes", "no"],
        Field(..., description="Has housing loan?")
    ]
    loan: Annotated[
        Literal["yes", "no"],
        Field(..., description="Has personal loan?")
    ]
    contact: Annotated[
        Literal["cellular", "telephone"],
        Field(..., description="Contact communication type")
    ]
    day_of_week: Annotated[int, Field(..., ge=1, le=31, description="Day of the month when contact was made")]
    month: Annotated[
        Literal[
            "jan","feb","mar","apr","may","jun","jul",
            "aug","sep","oct","nov","dec"
        ],
        Field(..., description="Month of contact")
    ]
    duration: Annotated[int, Field(..., ge=0, description="Duration of last contact in seconds")]
    campaign: Annotated[int, Field(..., ge=0, description="Number of contacts during this campaign")]
    pdays: Annotated[int, Field(..., ge=-1, description="Days since last contact (999 = never)")]
    previous: Annotated[int, Field(..., ge=0, description="Number of previous contacts before this campaign")]
    poutcome: Annotated[
        Literal["success", "failure", "nonexistent"],
        Field(..., description="Outcome of previous marketing campaign")
    ]

  
   
    @field_validator("job", "marital", "education", "default",            # normalizers
                     "housing", "loan", "contact", "month", "poutcome")
    @classmethod
    def lowercase_strip(cls, v: str) -> str:
        return v.strip().lower()


    @computed_field
    @property
    def has_previous_contact(self) -> bool:
        """the client was contacted before"""
        return self.pdays != 999

    @computed_field
    @property
    def is_high_balance(self) -> bool:
        """if balance is above typical median (like~1000)"""
        return self.balance > 1000

    @computed_field
    @property
    def contact_intensity(self) -> str:
        """how intensely the client was contacted"""
        if self.campaign == 0:
            return "none"
        if self.campaign <= 2:
            return "low"
        if self.campaign <= 5:
            return "medium"
        return "high"
