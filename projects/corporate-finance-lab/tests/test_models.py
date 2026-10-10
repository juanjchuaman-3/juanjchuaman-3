from dataclasses import replace
import math
import numpy as np
import pytest
from model import Assumptions, integrated_forecast, dcf, sensitivity
from portfolio import demo_returns, metrics, min_variance_weights

def test_balances():
    rows=integrated_forecast(Assumptions())
    assert len(rows)==5
    assert all(abs(r["balance_check"])<1e-8 for r in rows)

def test_dcf_identity():
    x=dcf(Assumptions())
    assert math.isclose(x["enterprise_value"],x["pv_fcff"]+x["pv_terminal_value"])
    assert math.isclose(x["equity_value"],x["enterprise_value"]-x["net_debt"])

def test_invalid_g():
    with pytest.raises(ValueError):
        dcf(replace(Assumptions(),terminal_growth=.11))

def test_sensitivity():
    rows=sensitivity(Assumptions(),[.095,.115],[.03])
    assert rows[0]["equity_value"]>rows[1]["equity_value"]

def test_portfolio():
    names,r=demo_returns()
    w=min_variance_weights(r)
    assert len(names)==len(w) and np.all(w>=0) and np.isclose(w.sum(),1)
    m=metrics(r,w)
    assert m["historical_cvar_1d"]>=m["historical_var_1d"]
