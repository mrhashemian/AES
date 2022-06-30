from api.schemas.base_schema import BaseSchema
from typing import Optional


class UpdateUserChatSettingSchema(BaseSchema):
    order_process: Optional[bool] = True
    abandoned_cart: Optional[bool] = True

    def get_entity_data(self):
        return {"chat_settings": {"orderProcess": self.order_process, "abandonedCart": self.abandoned_cart}}
