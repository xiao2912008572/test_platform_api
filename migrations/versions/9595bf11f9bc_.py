"""empty message

Revision ID: 9595bf11f9bc
Revises: 4fb72080914a
Create Date: 2018-08-03 15:05:38.609877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9595bf11f9bc'
down_revision = '4fb72080914a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_api_result_param',
    sa.Column('paramID', sa.Integer(), nullable=False),
    sa.Column('paramName', sa.String(length=255), nullable=False),
    sa.Column('paramKey', sa.String(length=255), nullable=False),
    sa.Column('paramNotNull', sa.Boolean(), nullable=False),
    sa.Column('apiID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apiID'], ['eo_api.apiID'], ),
    sa.PrimaryKeyConstraint('paramID')
    )
    op.create_table('eo_api_result_value',
    sa.Column('valueID', sa.Integer(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('valueDescription', sa.String(length=255), nullable=True),
    sa.Column('paramID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paramID'], ['eo_api_result_param.paramID'], ),
    sa.PrimaryKeyConstraint('valueID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eo_api_result_value')
    op.drop_table('eo_api_result_param')
    # ### end Alembic commands ###
