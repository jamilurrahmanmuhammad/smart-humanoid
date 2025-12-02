"""Initial schema for RAG Chatbot Assistant

Revision ID: 001
Revises:
Create Date: 2025-12-02

Tables:
- chat_sessions: Conversation sessions with learners
- chat_messages: Individual messages with 24h retention
- citations: Source references for grounded answers
- analytics_events: Anonymized interaction metadata (no PII)
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create persona_type enum
    persona_type = sa.Enum(
        "Explorer", "Builder", "Engineer", "Default",
        name="persona_type"
    )
    persona_type.create(op.get_bind(), checkfirst=True)

    # Create message_role enum
    message_role = sa.Enum("user", "assistant", name="message_role")
    message_role.create(op.get_bind(), checkfirst=True)

    # Create query_type enum
    query_type = sa.Enum("global", "page", "selection", name="query_type")
    query_type.create(op.get_bind(), checkfirst=True)

    # Chat sessions table
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "persona",
            sa.Enum(
                "Explorer", "Builder", "Engineer", "Default",
                name="persona_type",
                create_constraint=False
            ),
            nullable=False,
            server_default="Default"
        ),
        sa.Column("current_chapter", sa.Integer, nullable=True),
        sa.Column("current_page", sa.String(255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column(
            "is_active",
            sa.Boolean,
            nullable=False,
            server_default=sa.sql.expression.true()
        ),
    )

    # Chat messages table
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "session_id",
            sa.String(36),
            sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column(
            "role",
            sa.Enum("user", "assistant", name="message_role", create_constraint=False),
            nullable=False
        ),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column(
            "query_type",
            sa.Enum(
                "global", "page", "selection",
                name="query_type",
                create_constraint=False
            ),
            nullable=False,
            server_default="global"
        ),
        sa.Column("selected_text", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column(
            "has_safety_disclaimer",
            sa.Boolean,
            nullable=False,
            server_default=sa.sql.expression.false()
        ),
    )
    # Index for expiration cleanup queries (FR-027)
    op.create_index(
        "idx_messages_expires_at",
        "chat_messages",
        ["expires_at"]
    )

    # Citations table
    op.create_table(
        "citations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "message_id",
            sa.String(36),
            sa.ForeignKey("chat_messages.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("chapter", sa.Integer, nullable=False),
        sa.Column("section", sa.String(100), nullable=False),
        sa.Column("heading", sa.String(200), nullable=False),
        sa.Column("quote", sa.String(500), nullable=False),
        sa.Column("link", sa.String(500), nullable=False),
        sa.Column("relevance_score", sa.Float, nullable=False),
    )

    # Analytics events table (no PII per FR-026)
    op.create_table(
        "analytics_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("message_id", sa.String(36), nullable=False, unique=True),
        sa.Column(
            "timestamp",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column("persona", sa.String(20), nullable=False),
        sa.Column("chapter", sa.Integer, nullable=True),
        sa.Column("query_type", sa.String(20), nullable=False),
        sa.Column("has_citations", sa.Boolean, nullable=False),
        sa.Column("has_safety_disclaimer", sa.Boolean, nullable=False),
        sa.Column("response_latency_ms", sa.Integer, nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
    )
    # Indexes for analytics cleanup and querying
    op.create_index(
        "idx_analytics_expires_at",
        "analytics_events",
        ["expires_at"]
    )
    op.create_index(
        "idx_analytics_timestamp",
        "analytics_events",
        ["timestamp"]
    )


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_index("idx_analytics_timestamp", table_name="analytics_events")
    op.drop_index("idx_analytics_expires_at", table_name="analytics_events")
    op.drop_table("analytics_events")

    op.drop_table("citations")

    op.drop_index("idx_messages_expires_at", table_name="chat_messages")
    op.drop_table("chat_messages")

    op.drop_table("chat_sessions")

    # Drop enums
    sa.Enum(name="query_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="message_role").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="persona_type").drop(op.get_bind(), checkfirst=True)
