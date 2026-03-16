from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", default=True, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="NO ACTION",
            ondelete="CASCADE",
            name="post_user_fkey",
        ),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )

    user = relationship("Users")


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )


class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer,
        ForeignKey(
            "posts.id",
            onupdate="NO ACTION",
            on_delete="CASCADE",
            name="votes_post_fkey",
        ),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="NO ACTION",
            on_delete="CASCADE",
            name="votes_user_fkey",
        ),
        primary_key=True,
        nullable=False,
    )
