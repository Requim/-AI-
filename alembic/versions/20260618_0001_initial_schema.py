"""initial schema

Revision ID: 20260618_0001
Revises:
Create Date: 2026-06-18
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260618_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """创建一期业务表。"""
    _create_orders()
    _create_shipments()
    _create_tracking_events()
    _create_inventory_forecasts()
    _create_profit_results()
    _create_task_statuses()


def downgrade() -> None:
    """删除一期业务表。"""
    for table in _tables():
        op.drop_table(table)


def _create_orders() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("sku", sa.String(length=128), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("destination", sa.JSON(), nullable=False),
        sa.Column("package", sa.JSON(), nullable=False),
        sa.Column("requirement", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_orders_order_id", "orders", ["order_id"], unique=True)


def _create_shipments() -> None:
    op.create_table(
        "shipments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("carrier", sa.String(length=64), nullable=False),
        sa.Column("service", sa.String(length=64), nullable=False),
        sa.Column("cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("estimated_days", sa.Integer(), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_shipments_order_id", "shipments", ["order_id"])


def _create_tracking_events() -> None:
    op.create_table(
        "tracking_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tracking_no", sa.String(length=128), nullable=False),
        sa.Column("carrier", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("latest_location", sa.String(length=255), nullable=False),
        sa.Column("alerts", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_tracking_events_tracking_no", "tracking_events", ["tracking_no"])


def _create_inventory_forecasts() -> None:
    op.create_table(
        "inventory_forecasts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sku", sa.String(length=128), nullable=False),
        sa.Column("region", sa.String(length=64), nullable=False),
        sa.Column("forecast_days", sa.Integer(), nullable=False),
        sa.Column("predicted_units", sa.Integer(), nullable=False),
        sa.Column("reorder_units", sa.Integer(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_inventory_forecasts_sku", "inventory_forecasts", ["sku"])


def _create_profit_results() -> None:
    op.create_table(
        "profit_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sku", sa.String(length=128), nullable=False),
        sa.Column("gross_profit", sa.Numeric(12, 2), nullable=False),
        sa.Column("net_profit", sa.Numeric(12, 2), nullable=False),
        sa.Column("profit_margin", sa.Numeric(8, 4), nullable=False),
        sa.Column("risk_items", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_profit_results_sku", "profit_results", ["sku"])


def _create_task_statuses() -> None:
    op.create_table(
        "task_statuses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_name", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_task_statuses_task_name", "task_statuses", ["task_name"])


def _tables() -> list[str]:
    return [
        "task_statuses",
        "profit_results",
        "inventory_forecasts",
        "tracking_events",
        "shipments",
        "orders",
    ]
