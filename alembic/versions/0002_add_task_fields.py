
from alembic import op
import sqlalchemy as sa


revision = "add_task_fields"
down_revision = "baseline_tasks"
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table(
    "tasks",
    **batch_options(),
) as batch_op:
        dialect = op.get_bind().dialect.name

        completed_default = (
            sa.text("false")
            if dialect == "postgresql"
            else sa.text("0")
        )
        batch_op.add_column(
            sa.Column(
                "completed",
                sa.Boolean(),
                nullable=False,
                server_default=completed_default,
            )
        )

        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text(
                    "CURRENT_TIMESTAMP"
                ),
            )
        )


def downgrade():
    with op.batch_alter_table(
    "tasks",
    **batch_options(),
) as batch_op:
        batch_op.drop_column("created_at")
        batch_op.drop_column("completed")

def batch_options():
    if op.get_bind().dialect.name == "sqlite":
        return {
            "recreate": "always",
            "table_kwargs": {
                "sqlite_autoincrement": True
            },
        }

    return {"recreate": "never"}
