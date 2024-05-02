from pydantic import BaseModel
import services as svc_schemas


class User(BaseModel):
    login: str
    password: str

    def to_service_model(self):
        return svc_schemas.User(login=self.login, password=self.password)
