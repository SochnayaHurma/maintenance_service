"""create_main_tables
Revision ID: 21ac67a1d1af
Revises: 
Create Date: 2023-07-05 15:13:28.095484
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from typing import Tuple



# revision identifiers, used by Alembic
revision = '21ac67a1d1af'
down_revision = None
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed
        )
    )


def create_update_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def create_cleaning_tables() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", INTEGER(unsigned=True), primary_key=True),
        sa.Column("name", sa.VARCHAR(255), nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("processed", sa.Boolean, server_default="False", nullable=False),
        sa.Column("owner", INTEGER(unsigned=True), sa.ForeignKey("users.id", ondelete="CASCADE")),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_cleanings_modtime
            BEFORE UPDATE
            ON cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", INTEGER(unsigned=True), primary_key=True),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean, nullable=False, server_default="False"),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_profiles_table() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.VARCHAR(255), nullable=True),
        sa.Column("phone_number", sa.VARCHAR(255), nullable=True),
        sa.Column("bio", sa.Text, nullable=True, server_default=""),
        sa.Column("image", sa.VARCHAR(255), nullable=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_offers_table() -> None:
    op.create_table(
        "user_offers_for_cleanings",
        sa.Column(
            "uid",
            sa.String(length=255),
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            INTEGER(unsigned=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        sa.Column(
            "cleaning_id",
            INTEGER(unsigned=True),
            sa.ForeignKey("cleanings.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        ),
        sa.Column(
            "status",
            sa.VARCHAR(length=20),
            nullable=False,
            index=True,
            server_default="pending"
        ),
        *timestamps(),
    )
    #op.create_primary_key("pk_user_offers_for_cleanings", "user_offers_for_cleanings", ["user_id", "cleaning_id"])
    op.execute(
        """
        CREATE TRIGGER update_user_offers_for_cleanings_modtime
            BEFORE UPDATE
            on user_offers_for_cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_cleaner_evaluations_table() -> None:
    op.create_table(
        "cleaning_to_cleaner_evaluations",
        sa.Column(
            "cleaning_id",
            INTEGER(unsigned=True),
            sa.ForeignKey("cleanings.id", ondelete="SET NULL"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "cleaner_id",
            INTEGER(unsigned=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=False,
            index=True,
        ),
        sa.Column("no_show", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("headline", sa.VARCHAR(length=255), nullable=True),
        sa.Column("comment", sa.VARCHAR(length=510), nullable=True),
        sa.Column("professionalism", INTEGER, nullable=True),
        sa.Column("completeness", INTEGER, nullable=True),
        sa.Column("efficiency", INTEGER, nullable=True),
        sa.Column("overall_rating", INTEGER, nullable=False),
        *timestamps(),
    )
    op.create_primary_key(
        "pk_cleaning_to_cleaner_evaluations",
        "cleaning_to_cleaner_evaluations",
        ["cleaning_id", "cleaner_id"],
    )
    op.execute(
        """
        CREATE TRIGGER update_cleaning_to_cleaner_evaluations
            BEFORE UPDATE
            ON cleaning_to_cleaner_evaluations
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_update_at_trigger()
    create_users_table()
    create_profiles_table()
    create_cleaning_tables()
    create_offers_table()
    create_cleaner_evaluations_table()


def downgrade() -> None:
    op.drop_table("cleaning_to_cleaner_evaluations")
    op.drop_table("user_offers_for_cleanings")
    op.drop_table("cleanings")
    op.drop_table("profiles")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
