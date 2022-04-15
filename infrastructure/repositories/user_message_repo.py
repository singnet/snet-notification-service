from datetime import datetime as dt
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import UserMessage


class UserMessageHistoryRepo(BaseRepository):

    def add_message(self, source, name, address, email, phone_no, message_type, subject, message):
        self.add_item(
            UserMessage(
                source=source,
                name=name,
                address=address,
                email=email,
                phone_no=phone_no,
                message_type=message_type,
                subject=subject,
                message=message,
                created_at=dt.utcnow(),
                updated_at=dt.utcnow()

            )
        )
