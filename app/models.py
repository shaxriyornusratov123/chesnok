from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id"), nullable=True
    )
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    posts_count: Mapped[int] = mapped_column(BigInteger, default=0)
    posts_read_count: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="users"
    )
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")

    def __repr__(self):
        return f"User({self.first_name} {self.last_name})"


class Post(BaseModel):
    __tablename__ = "post"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    mins_read: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    postmedia: Mapped[list["PostMedia"]] = relationship(
        "PostMedia", back_populates="post"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"{self.title}"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")

    def __repr__(self):
        return f"Category({self.name})"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    def __repr__(self):
        return f"Category({self.name})"


class Profession(Base):
    __tablename__ = "professions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped["User"] = relationship("User", back_populates="profession")

    def __repr__(self):
        return f"Profession({self.name})"


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String(100))

    postmedia: Mapped[list["PostMedia"]] = relationship(
        "PostMedia", back_populates="media"
    )

    def __repr__(self):
        return f"Media({self.url})"


class PostMedia(Base):
    __tablename__ = "post_media"

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)

    post: Mapped["Post"] = relationship("Post", back_populates="postmedia")
    media: Mapped["Media"] = relationship("Media", back_populates="postmedia")


class Comment(BaseModel):
    __tablename__ = "comments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"Comment({self.text})"
