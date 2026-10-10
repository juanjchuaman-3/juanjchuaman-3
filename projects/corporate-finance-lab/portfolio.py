"""Illustrative portfolio analytics using deterministic, synthetic returns."""
import numpy as np

def demo_returns(days: int = 756, seed: int = 2026):
    rng=np.random.default_rng(seed)
    assets=["US Equity","Dev Equity","EM Equity","Treasury","Gold"]
    vols=np.array([.17,.18,.23,.065,.16])/np.sqrt(252)
    means=np.array([.08,.065,.085,.032,.045])/252
    factors=rng.normal(size=(days,3))
    exposures=np.array([[.85,.20,0],[.75,.35,0],[.7,.5,0],[-.2,0,.5],[0,.1,.5]])
    shock=factors@exposures.T+rng.normal(scale=.50,size=(days,5))
    shock=(shock-shock.mean(axis=0))/shock.std(axis=0)
    return assets,means+shock*vols

def metrics(returns,weights,annual_rf=.03,confidence=.95):
    """Annual arithmetic moments; 1-day historical VaR/CVaR on notional 1."""
    r=np.asarray(returns,dtype=float)
    w=np.asarray(weights,dtype=float)
    if r.ndim!=2 or r.shape[1]!=w.size or r.shape[0]<3:
        raise ValueError("Returns matrix/weights dimensions invalid")
    if not np.all(np.isfinite(r)) or np.any(w<-1e-10) or not np.isclose(w.sum(),1):
        raise ValueError("Invalid weights or data")
    port=r@w  # assumes daily constant-weight rebalancing
    ann_ret=port.mean()*252
    ann_vol=port.std(ddof=1)*np.sqrt(252)
    sharpe=(ann_ret-annual_rf)/ann_vol if ann_vol else np.nan
    cutoff=np.quantile(port,1-confidence)
    return dict(annual_return=ann_ret,annual_volatility=ann_vol,sharpe=sharpe,
        historical_var_1d=max(0.,-cutoff),
        historical_cvar_1d=max(0.,-port[port<=cutoff].mean()))

def min_variance_weights(returns):
    """No-short SLSQP minimum variance; purely in-sample."""
    from scipy.optimize import minimize
    r=np.asarray(returns,dtype=float)
    cov=np.cov(r,rowvar=False)
    n=r.shape[1]
    opt=minimize(lambda w:w@cov@w,np.repeat(1/n,n),
        bounds=[(0,1)]*n,
        constraints=[{"type":"eq","fun":lambda w:w.sum()-1}],
        method="SLSQP",options={"ftol":1e-14,"maxiter":3000})
    if not opt.success:
        raise RuntimeError(opt.message)
    w=np.clip(opt.x,0,1)
    return w/w.sum()
