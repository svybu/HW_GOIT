import aiohttp
import asyncio
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--exchange', metavar='days', type=int, default=5, help="Number of days to check")
parser.add_argument('--currency', metavar='currency', type=str, help="additional currency")
args = parser.parse_args()
days_to_check = args.exchange
currency = args.currency.upper() if args.currency else None


async def fetch_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["exchangeRate"]
            else:
                print(f"Error fetching data for date {date}: {response.status}")
                return None


def display_rates(rates, currency=None):
    rates_dict = {rate["currency"]: rate.get("purchaseRate") for rate in rates}
    print(f'USD : {rates_dict.get("USD")}')
    print(f'EUR : {rates_dict.get("EUR")}')
    if currency:
        print(f'{currency} : {rates_dict.get(currency, "Not available")}')


async def days(days_to_check=1):
    current_date = datetime.date.today()
    if days_to_check <= 10:
        for i in range(days_to_check):
            date_to_check = current_date - datetime.timedelta(days=i)
            rates = await fetch_exchange_rates(date_to_check)
            if rates:
                print(f"Exchange rates for {date_to_check}:")
                display_rates(rates, currency)
            else:
                print(f"Error fetching data for date {date_to_check}")
    else:
        print('Too far from current date')


if __name__ == "__main__":
    r = asyncio.run(days(days_to_check))
