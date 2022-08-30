"""init

Revision ID: 8109a62e55d4
Revises: 
Create Date: 2022-08-26 12:48:41.640006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8109a62e55d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_offer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(length=256), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('company_name', sa.String(length=256), nullable=True),
    sa.Column('earning_value_from', sa.Integer(), nullable=True),
    sa.Column('earning_value_to', sa.Integer(), nullable=True),
    sa.Column('contract_type', sa.String(length=64), nullable=True),
    sa.Column('seniority', sa.String(length=64), nullable=True),
    sa.Column('offer_deadline', sa.Date(), nullable=True),
    sa.Column('working_mode', sa.String(length=64), nullable=True),
    sa.Column('working_time', sa.String(length=64), nullable=True),
    sa.Column('remote_recruitment', sa.Boolean(), nullable=True),
    sa.Column('immediate_employment', sa.Boolean(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('link')
    )
    op.create_index(op.f('ix_job_offer_id'), 'job_offer', ['id'], unique=False)
    op.create_table('benefit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('benefit', sa.String(length=2048), nullable=True),
    sa.Column('job_offer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_offer_id'], ['job_offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_benefit_id'), 'benefit', ['id'], unique=False)
    op.create_table('requirement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requirement', sa.String(length=2048), nullable=True),
    sa.Column('must_have', sa.Boolean(), nullable=True),
    sa.Column('job_offer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_offer_id'], ['job_offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requirement_id'), 'requirement', ['id'], unique=False)
    op.create_table('responsibility',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('responsibility', sa.String(length=2048), nullable=True),
    sa.Column('job_offer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_offer_id'], ['job_offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_responsibility_id'), 'responsibility', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_responsibility_id'), table_name='responsibility')
    op.drop_table('responsibility')
    op.drop_index(op.f('ix_requirement_id'), table_name='requirement')
    op.drop_table('requirement')
    op.drop_index(op.f('ix_benefit_id'), table_name='benefit')
    op.drop_table('benefit')
    op.drop_index(op.f('ix_job_offer_id'), table_name='job_offer')
    op.drop_table('job_offer')
    # ### end Alembic commands ###
