"""Initial migration

Revision ID: 345e5fd4f6ac
Revises: 
Create Date: 2024-12-31 15:52:10.693054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '345e5fd4f6ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID NOT NULL,
            email VARCHAR NOT NULL,
            hashed_password VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            PRIMARY KEY (id),
            UNIQUE (email)
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS debts (
            id UUID NOT NULL,
            title VARCHAR NOT NULL,
            amount FLOAT NOT NULL,
            due_date DATE NOT NULL,
            status VARCHAR DEFAULT 'pendente',
            observations VARCHAR,
            user_id UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('debts')
    op.drop_table('users')
    # ### end Alembic commands ###
