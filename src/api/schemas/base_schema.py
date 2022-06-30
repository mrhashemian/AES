from pydantic import BaseModel


class BaseSchema(BaseModel):
    # class Config:
    #     extra = "allow"

    def to_model(self):
        model = self
        return model

    def rename_attribute(self, old_name, new_name):
        self.__dict__[new_name] = self.__dict__.pop(old_name)

    def delete_attribute(self, name):
        delattr(self, name)
