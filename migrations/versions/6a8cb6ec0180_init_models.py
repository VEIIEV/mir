"""init models

Revision ID: 6a8cb6ec0180
Revises:
Create Date: 2023-07-29 15:22:20.958378

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from src.questionnaire.params_choice import BodyType, Gender, Goal, Passion

# revision identifiers, used by Alembic.
revision = "6a8cb6ec0180"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_delete", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_user_email"), "auth_user", ["email"], unique=True)
    op.create_table(
        "black_list_user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("blocked_by_id", sa.Uuid(), nullable=False),
        sa.Column("blocked_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("NOT(blocked_by_id = blocked_id)", name="_black_list_cc"),
        sa.ForeignKeyConstraint(
            ["blocked_by_id"], ["auth_user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["blocked_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("blocked_by_id", "blocked_id", name="_black_list_uc"),
    )
    op.create_table(
        "match",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user1_id", sa.Uuid(), nullable=False),
        sa.Column("user2_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user1_id"], ["auth_user.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user2_id"], ["auth_user.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "message",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("message_text", sa.String(), nullable=False),
        sa.Column("sender_id", sa.Uuid(), nullable=False),
        sa.Column("receiver_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("NOT(sender_id = receiver_id)", name="_message_cc"),
        sa.ForeignKeyConstraint(["receiver_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_like",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("liked_user_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("NOT(user_id = liked_user_id)", name="_user_like_cc"),
        sa.ForeignKeyConstraint(
            ["liked_user_id"], ["auth_user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "liked_user_id", name="_user_like_uc"),
    )
    op.create_table(
        "user_questionnaire",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("firstname", sa.String(length=256), nullable=False),
        sa.Column("lastname", sa.String(length=256), nullable=True),
        sa.Column(
            "gender", sqlalchemy_utils.types.choice.ChoiceType(Gender), nullable=True
        ),
        sa.Column("photo", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("latitude", sa.Numeric(precision=8, scale=5), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=8, scale=5), nullable=True),
        sa.Column("about", sa.String(), nullable=True),
        sa.Column(
            "passion", sqlalchemy_utils.types.choice.ChoiceType(Passion), nullable=True
        ),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column(
            "goals", sqlalchemy_utils.types.choice.ChoiceType(Goal), nullable=True
        ),
        sa.Column(
            "body_type",
            sqlalchemy_utils.types.choice.ChoiceType(BodyType),
            nullable=True,
        ),
        sa.Column("is_visible", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_settings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("subscriber", sa.DateTime(), nullable=True),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_settings")
    op.drop_table("user_questionnaire")
    op.drop_table("user_like")
    op.drop_table("message")
    op.drop_table("match")
    op.drop_table("black_list_user")
    op.drop_index(op.f("ix_auth_user_email"), table_name="auth_user")
    op.drop_table("auth_user")
    # ### end Alembic commands ###
