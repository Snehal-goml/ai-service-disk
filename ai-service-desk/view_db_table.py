import sqlite3

DB_PATH = "servicedesk.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all tickets
cursor.execute("SELECT id, title, priority, status, assignee_email, created_at FROM tickets;")
rows = cursor.fetchall()

print(f"\n{'='*120}")
print(f"{'TICKETS DATABASE':^120}")
print(f"{'='*120}\n")

# Table header
print(f"{'#':<4} {'ID':<38} {'Title':<20} {'Priority':<12} {'Status':<10} {'Assignee':<25} {'Created At'}")
print(f"{'-'*4} {'-'*38} {'-'*20} {'-'*12} {'-'*10} {'-'*25} {'-'*19}")

# Table rows
for idx, row in enumerate(rows, 1):
    ticket_id, title, priority, status, assignee, created_at = row
    assignee = assignee if assignee else 'None'
    created_at = created_at[:19] if created_at else 'None'  # Trim microseconds
    
    print(f"{idx:<4} {ticket_id:<38} {title:<20} {priority:<12} {status:<10} {assignee:<25} {created_at}")

print(f"\n{'='*120}")
print(f"Total tickets: {len(rows)}")
print(f"{'='*120}\n")

conn.close()