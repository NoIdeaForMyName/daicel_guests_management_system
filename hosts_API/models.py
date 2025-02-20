from pydantic import BaseModel

class FullHost(BaseModel, frozen=True):
    id: int
    firstname: str
    lastname: str
    def __str__(self):
        return f'{self.id} - {self.firstname} {self.lastname}'
