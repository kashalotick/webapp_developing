from app.exceptions import ErrorSchema


class ResponseDoc:

    def __init__(self) -> None:
        self.responses = {}


    def _response_value(self, description: str):
        return  {"description": description, "model": ErrorSchema}
    def not_found_404(self) -> "ResponseDoc":
        self.responses.update({404: self._response_value("Not found")})
        return self

    def not_authorized_401(self) -> "ResponseDoc":
        self.responses.update({401: self._response_value("Not authorized")})
        return self
    def method_not_allowed_405(self) -> "ResponseDoc":
        self.responses.update({405: self._response_value("Method not allowed")})
        return self

    def conflict_409(self) -> "ResponseDoc":
        self.responses.update({409: self._response_value("Conflict")})
        return self

    def add(self, status:int | str, description: str) -> "ResponseDoc":
        self.responses.update({status: self._response_value(description)})
        return self

    def get_dict(self):
        return self.responses