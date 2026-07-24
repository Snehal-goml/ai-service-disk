import asyncio
import sys
sys.path.insert(0, ".")

from sqlalchemy import text
from app.core.database import engine

async def view_table():
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT id, title, priority, status, assignee_email, created_at FROM tickets ORDER BY created_at DESC;")
        )
        rows = result.fetchall()

    print(f"\n{'='*120}")
    print(f"{'POSTGRESQL TICKETS DATABASE':^120}")
    print(f"{'='*120}\n")

    print(f"{'#':<4} {'ID':<38} {'Title':<20} {'Priority':<12} {'Status':<10} {'Assignee':<25} {'Created At'}")
    print(f"{'-'*4} {'-'*38} {'-'*20} {'-'*12} {'-'*10} {'-'*25} {'-'*19}")

    for idx, row in enumerate(rows, 1):
        ticket_id, title, priority, status, assignee, created_at = row
        assignee = assignee if assignee else 'None'
        created_str = str(created_at)[:19] if created_at else 'None'
        print(f"{idx:<4} {str(ticket_id):<38} {str(title):<20} {str(priority):<12} {str(status):<10} {str(assignee):<25} {created_str}")

    print(f"\n{'='*120}")
    print(f"Total tickets: {len(rows)}")
    print(f"{'='*120}\n")

if __name__ == "__main__":
    asyncio.run(view_table())