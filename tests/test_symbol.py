"""Integration tests for the symbol-related functions."""

import pytest
from enum import Enum

from mt4client.api import Symbol, StandardTimeframe
from mt4client import MT4Client


@pytest.fixture(scope="module")
def symbol(mt4: MT4Client, symbol_name: str) -> Symbol:
    return mt4.symbol(symbol_name)


def test_symbol_tick(symbol: Symbol):
    tick = symbol.tick
    assert isinstance(tick.time, int)
    assert isinstance(tick.bid, float)
    assert isinstance(tick.ask, float)
    assert isinstance(tick.last, float)
    assert isinstance(tick.volume, int)


def test_fetch_ohlcv(symbol: Symbol):
    ohlcv = symbol.ohlcv("1h", 100)
    assert isinstance(ohlcv, list)
    assert len(ohlcv) == 100
    print(f"Found {len(ohlcv)} OHLCV bars. The first one: {ohlcv[0]}")


def test_symbol_names(mt4: MT4Client):
    symbol_names = mt4.symbol_names()
    assert isinstance(symbol_names, list)
    print(f"All symbols: {symbol_names}")


def test_symbols(mt4: MT4Client):
    symbols = mt4.symbols(*mt4.symbol_names()[0:3])
    assert isinstance(symbols, dict)
    assert len(symbols) == 3
    print(f"Found {len(symbols)} symbols. The first one: {next(iter(symbols.items()))}")


def test_indicator(mt4: MT4Client, symbol: Symbol):
    func = "iAC"
    args = [symbol.name, StandardTimeframe.PERIOD_H1.value, 1]
    result = mt4.indicator(func, args)
    assert isinstance(result, float)
    print(f"{func}({str(args)[1:-1]}) = {result}")
