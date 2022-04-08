from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, func, text, DECIMAL
from sqlalchemy.dialects.mysql import JSON, TIMESTAMP, VARCHAR, TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
created_at_default = func.current_timestamp()
updated_at_default = func.current_timestamp()


class UserMessage(Base):
    __tablename__ = "user_message"
    id = Column("row_id", Integer, primary_key=True, autoincrement=True)
    source = Column("source", VARCHAR(128), nullable=False)
    name = Column("name", VARCHAR(128), nullable=True)
    address = Column("address", VARCHAR(128), nullable=True)
    email = Column("email", VARCHAR(128), nullable=True)
    phone_no = Column("phone_no", VARCHAR(64), nullable=True)
    message_type = Column("message_type", VARCHAR(64), nullable=False)
    subject = Column("subject", VARCHAR(512), nullable=True)
    message = Column("message", TEXT, nullable=False)
    created_at = Column("created_at", TIMESTAMP, server_default=created_at_default, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, server_default=updated_at_default, nullable=False)
