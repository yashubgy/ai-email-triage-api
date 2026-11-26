from google import genai
from google.genai import types
from expected_type import EmailInput,EmailTriageResult

class EmailClassifier:
    def __init__(self , api_key : str ):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("No Api Key Found!! ")
        self.client = genai.Client(api_key = self.api_key)
        self.model = "gemini-3.5-flash-lite"

    def classify(self, email : EmailInput):
        prompt =(f"Analyze this email and classify it accurately"
                 f"From : {email.sender}"
                 f"Subject : {email.subject}"
                 f"Body : {email.body}")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an executive email triage assistant. "
                    "Be strict with priority scores: only give 5 to true emergencies, "
                    "server outages, or time-sensitive deadlines."
                ),
                response_mime_type="application/json",
                response_schema=EmailTriageResult,
                temperature=0.1,
            ),
        )

        return response.parsed #parsed convert the json in to pydantic obj

if __name__ == "__main__":
    classifier = EmailClassifier(api_key="Enter your api key")
    sample_email = EmailInput(
        sender="info@puma.com",
        subject="Support Help",
        body="Dear Yashu ,Thank you for your continued correspondence.Further to our previous communications, we would like to once again clarify that PUMA does not provide or authorize jersey customization, printing, or personalization services at this location. This policy remains consistent across our stores (except select locations in Bangalore.As informed earlier, any reference to third-party vendors was shared purely as general guidance to help you explore external options. However, such vendors operate independently and are not affiliated with or authorized by PUMA in any manner.We would like to reiterate that we are unable to take responsibility for, or provide support on, any services availed through external providers. Additionally, any alterations carried out outside PUMA may impact the product’s warranty and eligibility for return or exchange, as per our policy. As this has been communicated multiple times, we regret to inform you that we will not be able to assist further on this request, and the case will be considered closed from our end.We appreciate your understanding , Please leave a review for us"
    )
    result = classifier.classify(sample_email)

    print("Category      :", result.category)
    print("Priority (1-5):", result.priority_score)
    print("Needs Reply?  :", result.reply_need)
    print("Summary       :", result.summary)
    print("Draft Reply   :", result.suggested_reply)


    