import asyncio
import cProfile
import pstats
import time
from app.core.database import AsyncSessionLocal, Base, engine
from app.services.ticket_service import TicketService
from app.main import home, health, ready


async def run_benchmark():
    print("=== Running Performance Benchmark & Profiling ===")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 1. Benchmark sync functions
    start = time.perf_counter()
    for _ in range(1000):
        home()
        health()
    sync_duration = (time.perf_counter() - start) * 1000
    print(f"[SYNC] home & health (1,000 calls): {sync_duration:.2f} ms")

    # 2. Benchmark async ticket service operations
    async with AsyncSessionLocal() as session:
        service = TicketService(session)
        
        # ready check
        await ready(session)

        # TicketService.create
        t0 = time.perf_counter()
        tickets = []
        for i in range(50):
            t = await service.create({"title": f"Profile Ticket {i}", "priority": "high"})
            tickets.append(t)
        create_duration = (time.perf_counter() - t0) * 1000
        print(f"[ASYNC] TicketService.create (50 ops): {create_duration:.2f} ms")

        # TicketService.list_tickets
        t0 = time.perf_counter()
        for _ in range(20):
            await service.list_tickets()
        list_duration = (time.perf_counter() - t0) * 1000
        print(f"[ASYNC] TicketService.list_tickets (20 queries): {list_duration:.2f} ms")

        # TicketService.update & close
        t0 = time.perf_counter()
        for t in tickets:
            await service.update(t.id, {"priority": "low"})
            await service.close(t.id)
        update_duration = (time.perf_counter() - t0) * 1000
        print(f"[ASYNC] TicketService.update & close (100 ops): {update_duration:.2f} ms")

        # TicketService.delete
        t0 = time.perf_counter()
        for t in tickets:
            await service.delete(t.id)
        delete_duration = (time.perf_counter() - t0) * 1000
        print(f"[ASYNC] TicketService.delete (50 ops): {delete_duration:.2f} ms")


def main():
    profiler = cProfile.Profile()
    profiler.enable()
    
    asyncio.run(run_benchmark())
    
    profiler.disable()
    
    print("\n" + "="*60)
    print("         cProfile TOP 20 CUMULATIVE TIME CONSUMPTION")
    print("="*60)
    profiler.dump_stats("profile_results.prof")
    print("Saved profile data to profile_results.prof")

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(20)


if __name__ == "__main__":
    main()
