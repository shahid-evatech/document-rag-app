from pydantic import BaseModel, Field

# 📥 This handles the incoming data format from the user/frontend
class AskRequest(BaseModel):
    question: str = Field(..., example="What is our Q3 growth target?")

# 📤 These handle the outgoing response formats for Swagger documentation
class UploadSuccessResponse(BaseModel):
    status: str = Field(example="success")
    message: str = Field(example="Successfully parsed and indexed 14 document chunks.")
    filename: str = Field(example="financial_report.pdf")

class QueryAnswerResponse(BaseModel):
    query: str = Field(example="What is our Q3 growth target?")
    answer: str = Field(example="Our Q3 growth target is 12% quarter-over-quarter.")
    source_chunk: str = Field(example="...based on regional expansion, the target for Q3 is set firmly at 12%...")