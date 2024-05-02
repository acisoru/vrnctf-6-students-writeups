from pydantic import BaseModel
import services.schemas as svc_schemas


class Feedback(BaseModel):
    message_text: str

    def to_service_model(self):
        return svc_schemas.Feedback(
            sender_login=self.sender_login, message_text=self.message_text
        )
