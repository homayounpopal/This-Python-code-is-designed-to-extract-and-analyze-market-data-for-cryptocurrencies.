import requests
import pandas as pd
import time
from rich.console import Console
from rich.table import Table

console = Console()


def fetch_market_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    return response.json()


def analyze_market(df):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("نام ارز", style="cyan")
    table.add_column("(u)", style="cyan")  # اینجا نقطه ورود
    table.add_column("حد ضرر (u)", style="cyan")
    table.add_column("هدف سود (u)", style="cyan")
    table.add_column("تایم فریم", style="cyan")
    table.add_column("اهرم", style="cyan")  # اینجا اهرم

    for index, row in df.iterrows():
        entry_point = row['current_price']  # نقطه ورود
        stop_loss = entry_point * 0.98  # حد ضرر 2% زیر قیمت ورود
        take_profit = entry_point * 1.05  # هدف سود 5% بالاتر از قیمت ورود
        time_frame = '1H'  # تایم فریم
        leverage = 5  # اهرم

        # اضافه کردن ردیف به جدول
        table.add_row(
            row['name'],
            f"${entry_point:.2f}",  # نقطه ورود
            f"${stop_loss:.2f}",  # حد ضرر
            f"${take_profit:.2f}",  # هدف سود
            time_frame,  # تایم فریم
            str(leverage)  # اهرم
        )

    console.print(table)


while True:
    data = fetch_market_data()
    df = pd.DataFrame(data)

    analyze_market(df)

    time.sleep(120)  # هر 120 ثانیه یکبار داده‌ها را به‌روزرسانی کن