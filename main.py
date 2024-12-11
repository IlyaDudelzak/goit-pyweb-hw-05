from datetime import datetime, date, timedelta
from sys import argv
import platform
import aiohttp
import asyncio

days=2

try:
    if(int(argv[1]) < 1 or int(argv[1]) > 10):
        print("Wrong day count argument! Use between 1 and 10 (default 2)")
        exit()
        
except ValueError:
    print("Day count is not an integer!")
    exit()

days = int(argv[1])

async def main():
    res = {}
    async with aiohttp.ClientSession() as session:
        today = datetime.now()
        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            async with session.get(f"https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5&date={date}") as response:
                res[date] = await response.json()
    return res

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)
 