"""
Module for handling order scheduling.
"""

from datetime import UTC, datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.order.models import Order, OrderStatus


class OrderScheduler:
    """Order scheduler class"""

    def __init__(self):
        """Initialize the scheduler"""
        self.scheduler = AsyncIOScheduler()
        self._setup()

    def _setup(self):
        """Configure scheduler jobs"""
        self.scheduler.add_job(
            self.cancel_old_orders,
            "interval",
            seconds=300,
            coalesce=True,
            max_instances=1,
        )

    async def cancel_old_orders(self):
        """Cancel orders older than 1 hour in bulk"""
        now = datetime.now(UTC)
        hour_ago = now - timedelta(hours=1)

        result = await Order.find(
            {
                "status": {"$in": [OrderStatus.PLACED, OrderStatus.READY]},
                "created_at": {"$lt": hour_ago},
            }
        ).update_many(
            {
                "$set": {
                    "status": OrderStatus.CANCELLED,
                    "updated_at": hour_ago + timedelta(hours=1),
                }
            }
        )

        print(f"Cancelled {result.modified_count} old orders")

    async def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        print("Order scheduler started")

    async def shutdown(self):
        """Graceful shutdown"""
        self.scheduler.shutdown()
        print("Order scheduler stopped")


order_scheduler = OrderScheduler()
