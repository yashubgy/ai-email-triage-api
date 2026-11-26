from typing import Literal
from pydantic import BaseModel , Field

class EmailInput(BaseModel):
    sender  : str
    subject : str
    body : str


class EmailTriageResult(BaseModel):
    category : Literal["Urgent" , "Billing" , "NewsLetter" , "Spam" , "Support" , "Refund" , "Update"] = Field(description= " Category for this Email.".title())
    priority_score : int = Field(ge = 1 , le =5 , description="Priority order from 1[Least Priority Needed] to 5 [Urgent / Important]. ".title())
    reply_need : bool = Field(description= "If user needs to respond or not. ".title())
    summary : str  = Field(description= "A short 1 line summary of what sender wants ".title())
    suggested_reply : str = Field(description= " A short polite reply to it , Leave blank if reply_need is False")