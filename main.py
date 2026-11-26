from expected_type import EmailInput,EmailTriageResult
from classifier import EmailClassifier
from fastapi import FastAPI , HTTPException

app = FastAPI(title = "Email Triage API" ,
              description= "Classifies, prioritizes, and drafts replies for incoming emails using Gemini.",
              version= "1.0.0")

classifier = EmailClassifier(api_key="Enter your api key")

@app.get("/health")
def health_check():
    
    return{"status" : "online", "model" : classifier.model}

@app.post("/classify" , response_model= EmailTriageResult)
def classify_single_email(email:EmailInput):
    try:
        result = classifier.classify(email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/classify-batch" , response_model= list[EmailTriageResult])
def classify_batch_emails(emails: list[EmailInput]):
    if not emails:
        raise HTTPException(status_code=400, detail="Email list cannot be empty.")
    results = []
    if emails:
        try:
            for e in emails:
                results.append(classifier.classify(emails))
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch classification failed: {str(e)}")

