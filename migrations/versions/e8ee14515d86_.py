"""empty message

Revision ID: e8ee14515d86
Revises: a9e6b8416db8
Create Date: 2018-08-03 10:41:12.807756

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e8ee14515d86'
down_revision = 'a9e6b8416db8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_api_request_param',
    sa.Column('paramID', sa.Integer(), nullable=False),
    sa.Column('paramName', sa.String(length=255), nullable=True),
    sa.Column('paramKey', sa.String(length=255), nullable=False),
    sa.Column('paramValue', sa.Text(), nullable=False),
    sa.Column('paramType', sa.Boolean(create_constraint=3), nullable=True),
    sa.Column('paramLimit', sa.String(length=255), nullable=True),
    sa.Column('paramNotNull', sa.Boolean(), nullable=False),
    sa.Column('apiID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apiID'], ['eo_api.apiID'], ),
    sa.PrimaryKeyConstraint('paramID')
    )
    op.drop_column('eo_api', 'apiNoteRaw')
    op.drop_column('eo_api', 'apiFailureMockType')
    op.drop_column('eo_api', 'apiNoteType')
    op.drop_column('eo_api', 'apiSuccessMockType')
    op.add_column('eo_api_header', sa.Column('headerValue', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('eo_api_header', 'headerValue')
    op.add_column('eo_api', sa.Column('apiSuccessMockType', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('eo_api', sa.Column('apiNoteType', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('eo_api', sa.Column('apiFailureMockType', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('eo_api', sa.Column('apiNoteRaw', mysql.TEXT(), nullable=True))
    op.drop_table('eo_api_request_param')
    # ### end Alembic commands ###