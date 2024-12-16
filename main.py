from datetime import datetime, timedelta
from sys import argv
import platform
import aiohttp
import asyncio
import pprint

days=2
currencies = ["EUR", "USD"]

async def date_list(start, length, frwd=True):
    for i in range(length):
        delta = timedelta(days=i)
        if(frwd):
            yield start + delta
        else:
            yield start - delta
    #raise StopIteration

async def date_to_string(date):
    return date.strftime("%d.%m.%Y")

async def check_arguments():
    try:
        if(int(argv[1]) < 1 or int(argv[1]) > 10):
            print("Wrong day count argument! Use between 1 and 10 (default 2)")
            exit()

    except ValueError:
        print("Day count is not an integer!")
        exit()
    
    if(len(argv) > 1):
        global days
        days = int(argv[1])

async def API_request(URL:str, date:datetime):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str.replace(URL, "%DATE%", await date_to_string(date))) as response:
                return await response.json()
    except aiohttp.client_exceptions.ClientConnectorDNSError:
        print("Cannot connect to the server!")
        exit()
        
async def data_collector():
    currency_data = {}
    async with aiohttp.ClientSession() as session:
        async for date in date_list(datetime.now(), days, False):
            data = (await API_request("https://api.privatbank.ua/p24api/exchange_rates?json&date=%DATE%", date))["exchangeRate"]
            current = {}
            for currency in data:
                if(currency["currency"] in currencies):
                    current[currency["currency"]] = {"sale": currency["saleRate"], "purchase": currency["purchaseRate"]}
            currency_data[await date_to_string(date)] = current
                    
    return currency_data

async def main():
    await check_arguments()
    pprint.pprint(await data_collector())

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
 