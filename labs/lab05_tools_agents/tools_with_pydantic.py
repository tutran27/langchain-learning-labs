from enum import Enum
from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError, model_validator

from labs.lab01_foundation.llm_model import GroqLLMModel

# 1. Enum: chỉ cho phép 3 mức ưu tiên
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class MeetingInput(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Tiêu đề cuộc họp")
    duration_minutes: int = Field(default=30, ge=15, le=180, description="Thời lượng từ 15 đến 180 phút")
    participants: list[str] = Field(min_length=1, description="Danh sách email người tham gia")
    priority: Priority = Priority.MEDIUM
    meeting_type: Literal["online", "offline"] = "online"
    location: str | None = None

    @model_validator(mode="after")
    def validate_location(self):
        if self.meeting_type == "offline" and not self.location:
            raise ValueError(
                "Cuộc họp offline phải có địa điểm."
            )

        return self

@tool(args_schema=MeetingInput)
def create_meeting(title: str, duration_minutes: int, participants: list[str], priority: Priority, meeting_type: str, location: str | None = None):
    """Create a meeting by title, duration, participants, priority, meeting_type and location"""
    return f"""Đã tạo cuộc họp có nội dung: 
    Title: {title}
    Duration: {duration_minutes} minutes
    Participants: {', '.join(participants)}
    Priority: {priority.value if isinstance(priority, Priority) else priority}
    Meeting Type: {meeting_type}
    Location: {location or 'N/A'}"""
    
def test_valid_input():
    print("================ Validate Input =================")
    result=create_meeting.invoke({
        "title": "Testmeeting",
        "duration_minutes": 30,
        "participants": ["email1", "email2"],
        "priority": "high",
        "meeting_type": "online",
        "location": "Meeting room 1"
    })
    print(result)

def test_invalid_input():
    print("================ Invalid Input ================")
    try:
        result=create_meeting.invoke(
            {
            "title": "Tád",
            "duration_minutes": 25,
            "participants": ["mail_1"],
            "priority": "high",
            "meeting_type": "offline",
            "location": ""
            }
        )
    except ValidationError as e:
        print("Validation thất bại:")
        for item in e.errors():
            field = " -> ".join(str(x) for x in item["loc"])
            print(f"- {field or 'model'}: {item['msg']}")
    

def test_model_call():
    llm=GroqLLMModel().groq_chat()
    model_with_tools = llm.bind_tools([create_meeting])

    response = model_with_tools.invoke(
        "Tạo cuộc họp online tên Review Sprint, "
        "thời lượng 45 phút, mời an@example.com, "
        "mức ưu tiên cao."
    )

    print("================== LLM Response ===============")
    print(response.content)
    print("================== Final Response ===============")
    print(response.additional_kwargs["tool_calls"])


if __name__ == "__main__":
    test_valid_input()
    test_invalid_input()
    test_model_call()