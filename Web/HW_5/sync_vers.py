import requests
import datetime

def fetch_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["exchangeRate"]
    else:
        print(f"Error fetching data for date {date}: {response.status_code}")
        return None

def get_usd_eur_rates(rates):
    result = {}
    for rate in rates:
        if rate["currency"] == "USD":
            result["USD"] = {"purchaseRate": rate.get("purchaseRate"), "saleRate": rate.get("saleRate")}
        elif rate["currency"] == "EUR":
            result["EUR"] = {"purchaseRate": rate.get("purchaseRate"), "saleRate": rate.get("saleRate")}
    return result

def days(days_to_check=5):
    current_date = datetime.date.today()
    for i in range(days_to_check):
        date_to_check = current_date - datetime.timedelta(days=i)
        rates = fetch_exchange_rates(date_to_check)
        if rates:
            usd_eur_rates = get_usd_eur_rates(rates)
            print(f"Exchange rates for {date_to_check}:")
            print(usd_eur_rates)
        else:
            print(f"Error fetching data for date {date_to_check}")


if __name__ == "__main__":
    days()

