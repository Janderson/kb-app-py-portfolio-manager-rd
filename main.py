# -*- coding: utf-8 -*-
"""
@author: Janderson FFerreira
"""
import click
from core.markowitz import run_markowitz, run_markowitz_from_data_service, run_markowitz_with_leverage_from_data_service
from datetime import date, timedelta

VERSION = "1.1"


@click.group()
def cli():
    pass


@cli.command("markowitz")
@click.argument("stocks", default='BOVA11.SA,SMAL11.SA')
@click.option("--start-date", "start_date", default=None)
def cmd_run_markowitz(stocks, start_date: str):
    if not start_date:
        start_date = (date.today() - (timedelta(days=365)*5)).isoformat()
    else:
        start_date = start_date
    print(f"SIMULADOR MARKOWITZ  feito por Janderson FFerreira v{VERSION}\n\n")
    print(f"ativos: {stocks}")
    print(f"data inicio: {start_date}")
    print(f"data fim: {date.today()}")

    stocks = stocks.split(",")
    run_markowitz_from_data_service(stocks=stocks, 
                                    start_date=start_date)


@cli.command("markowitz_with_leverage")
@click.argument("stocks", default='BOVA11.SA,SMAL11.SA')
@click.option("--start-date", "start_date", default=None)
@click.option("--expected_return", "expected_return", default=None, type=click.FLOAT)
def cmd_run_markowitz(stocks, start_date: str, expected_return:float):
    if not start_date:
        start_date = (date.today() - (timedelta(days=365)*5)).isoformat()
    else:
        start_date = start_date
    print(f"SIMULADOR MARKOWITZ  feito por Janderson FFerreira v{VERSION}\n\n")
    print(f"ativos: {stocks}")
    print(f"data inicio: {start_date}")
    print(f"data fim: {date.today()}")

    stocks = stocks.split(",")
    run_markowitz_with_leverage_from_data_service(stocks=stocks, 
                                                  start_date=start_date,
                                                  expected_return=expected_return)


@cli.command("download_yfinance")
@click.argument("stocks", default='BOVA11,SMAL11')
@click.option("--start-date", "start_date", default=None)
def cmd_download_yf(stocks, start_date: str):
    from core.data_service import DataService, DataServiceParams
    if not start_date:
        start_date = (date.today() - (timedelta(days=365)*5)).isoformat()
    else:
        start_date = start_date
    print(f"SIMULADOR MARKOWITZ feito por Janderson FFerreira v{VERSION}\n\n")
    print(f"ativos: {stocks}")
    print(f"data inicio: {start_date}")
    print(f"data fim: {date.today()}")

    params = DataServiceParams(tickers=stocks.split(","),
                               start_date=start_date)

    data_service = DataService(params)
    data_service.load()
    data_service.save_prices()


if __name__ == "__main__":
    cli()
