"""Message and analytics purge service.

Background task service for cleaning up expired data per FR-027.
"""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession


class PurgeService:
    """Service for purging expired messages and analytics.

    Implements FR-027: 24-hour message TTL with automatic cleanup.
    """

    # TTL constant per FR-027
    MESSAGE_TTL_HOURS = 24

    async def purge_expired_messages(self, session: AsyncSession) -> int:
        """Delete messages where expires_at < current time.

        Args:
            session: Async database session.

        Returns:
            Number of messages deleted.

        FR Reference: FR-027 (24-hour message retention)
        """
        # Use raw SQL for efficient bulk delete
        query = text("""
            DELETE FROM chat_messages
            WHERE expires_at < :now
        """)

        result = await session.execute(
            query,
            {"now": datetime.now(timezone.utc)}
        )
        await session.commit()

        return result.rowcount

    async def purge_expired_analytics(self, session: AsyncSession) -> int:
        """Delete analytics events where expires_at < current time.

        Args:
            session: Async database session.

        Returns:
            Number of analytics events deleted.

        FR Reference: FR-027 (24-hour retention)
        """
        query = text("""
            DELETE FROM analytics_events
            WHERE expires_at < :now
        """)

        result = await session.execute(
            query,
            {"now": datetime.now(timezone.utc)}
        )
        await session.commit()

        return result.rowcount

    async def run_all(self, session: AsyncSession) -> dict[str, Any]:
        """Run all purge operations.

        Args:
            session: Async database session.

        Returns:
            Dictionary with deletion counts.
        """
        messages_deleted = await self.purge_expired_messages(session)
        analytics_deleted = await self.purge_expired_analytics(session)

        return {
            "messages_deleted": messages_deleted,
            "analytics_deleted": analytics_deleted,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
