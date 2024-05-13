from sqlalchemy import Column, Integer, BigInteger, String, event, text
from sqlalchemy.sql import func
import sqlalchemy

from core.database import Base


class RedirectInfo(Base):
    __tablename__ = "redirect_info"

    server_id = Column(BigInteger, primary_key=True, index=True)
    server_link = Column(String, nullable=False, unique=True, index=True)
    domen_link = Column(String, nullable=False, unique=True, index=True)
    last_use = Column(
        Integer,
        nullable=False,
        unique=False,
        server_default=func.extract("epoch", func.current_timestamp()),
    )
    updated_at = Column(
        Integer,
        nullable=False,
        unique=False,
        server_default=func.extract("epoch", func.current_timestamp()),
    )
    created_at = Column(
        Integer,
        nullable=False,
        unique=False,
        server_default=func.extract("epoch", func.current_timestamp()),
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


func_ = """
CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = EXTRACT(epoch FROM CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

trigger_exists_check_ = """
DO $$ 
BEGIN
    -- Check if the trigger exists
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'before_update_redirect_info') THEN
        -- Drop the existing trigger
        EXECUTE 'DROP TRIGGER before_update_redirect_info ON redirect_info';
    END IF;
END $$;
"""

trigger_create_ = """
CREATE TRIGGER before_update_redirect_info
BEFORE UPDATE ON redirect_info
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();
"""


@event.listens_for(RedirectInfo.__table__, "after_create")
def create_trigger(
    target: RedirectInfo.__table__, connection: sqlalchemy.engine.base.Connection, **kw
):
    connection.execute(text(func_))
    connection.execute(text(trigger_exists_check_))
    connection.execute(text(trigger_create_))
