import httpx

BASE = "http://127.0.0.1:8000"

print("=== Tickets in Database ===\n")

# Get all tickets
r = httpx.get(f"{BASE}/tickets")
if r.status_code == 200:
    tickets = r.json()
    print(f"Total tickets: {len(tickets)}\n")
    
    # Table header with better formatting
    print(f"{'#':<5} {'Title':<25} {'Priority':<12} {'Status':<12} {'Assignee':<25}")
    print("=" * 79)
    
    # Table rows with sequential numbering
    for idx, t in enumerate(tickets, 1):
        assignee = t['assignee_email'] or 'None'
        print(f"{idx:<5} {t['title']:<25} {t['priority']:<12} {t['status']:<12} {assignee:<25}")
else:
    print(f"Error: {r.status_code} - {r.text}")
    print("\nMake sure the server is running: uvicorn app.main:app --reload")
