"""empty message

Revision ID: a9e6b8416db8
Revises: 9c07926ac72e
Create Date: 2018-08-02 14:42:49.049101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e6b8416db8'
down_revision = '9c07926ac72e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_api_header',
    sa.Column('headerID', sa.Integer(), nullable=False),
    sa.Column('headerName', sa.String(length=255), nullable=False),
    sa.Column('apiID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apiID'], ['eo_api.apiID'], ),
    sa.PrimaryKeyConstraint('headerID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eo_api_header')
    # ### end Alembic commands ###
