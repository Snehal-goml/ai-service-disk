import asyncio
import asyncpg


async def main():
    # Connect to default postgres database as superuser
    # Try common default credentials
    credentials = [
        ("postgres", "postgres"),
        ("postgres", "admin"),
        ("postgres", ""),
    ]
    
    conn = None
    for user, password in credentials:
        try:
            dsn = f"postgresql://{user}:{password}@localhost:5432/postgres"
            conn = await asyncpg.connect(dsn)
            print(f"Connected as '{user}'")
            break
        except Exception as e:
            print(f"Failed as '{user}': {e}")
    
    if not conn:
        print("\nCould not connect to PostgreSQL. Please check your credentials.")
        return
    
    # Create user and database
    try:
        await conn.execute("CREATE USER snehal WITH PASSWORD 'snehal';")
        print("Created user 'snehal'")
    except Exception as e:
        print(f"User creation: {e}")
    
    try:
        await conn.execute("CREATE DATABASE servicedesk OWNER snehal;")
        print("Created database 'servicedesk'")
    except Exception as e:
        print(f"Database creation: {e}")
    
    try:
        await conn.execute("GRANT ALL PRIVILEGES ON DATABASE servicedesk TO snehal;")
        print("Granted privileges")
    except Exception as e:
        print(f"Privileges: {e}")
    
    await conn.close()
    print("\nSetup complete! Now run: python view_db.py")


if __name__ == "__main__":
    asyncio.run(main())