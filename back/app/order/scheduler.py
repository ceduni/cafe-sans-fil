import asyncio
from datetime import UTC, datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.order.models import Order, OrderStatus


async def cancel_old_orders():
    """Cancel orders older than 1 hour."""
    now = datetime.now(UTC)
    async for order in Order.find(
        {
            "$or": [{"status": OrderStatus.PLACED}, {"status": OrderStatus.READY}],
            "created_at": {"$lt": now - timedelta(hours=1)},
        }
    ):
        order.status = OrderStatus.CANCELLED
        order.updated_at = order.created_at + timedelta(hours=1)
        await order.save()


scheduler = AsyncIOScheduler()
scheduler.add_job(cancel_old_orders, "interval", seconds=60)
scheduler.start()

loop = asyncio.get_event_loop()
if not loop.is_running():
    loop.run_forever()
