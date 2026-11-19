"""量化研究共享基础库（纯标准库，零第三方依赖）。

供 cycle_clock / signal_synth / policy_multiplier / transmission / valuation /
market_sizing / stress_test / monte_carlo / threshold_calibration 共用。

设计约束（与实施方案一致）：
- 不引入 numpy / pandas / statsmodels（方案「依赖不可装则降级为手写最小二乘」条款），
  保证 CI 在仅安装 requirements.txt（openpyxl + markdown）时零新增依赖；
- 所有函数为纯函数：同输入同输出，无随机（蒙特卡洛的随机源由调用方注入并固定种子）；
- 时间序列输入统一为「记录列表」或「矩阵列表」，不依赖外部数据框。

线性代数：高斯消元（部分主元）求解线性方程组与矩阵求逆。
"""
from __future__ import annotations

import math
from typing import Sequence

# ---------------------------------------------------------------------------
# 基础统计
# ---------------------------------------------------------------------------


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def std(xs: Sequence[float], ddof: int = 1) -> float:
    """样本标准差（ddof=1）；样本不足返回 0。"""
    n = len(xs)
    if n - ddof <= 0:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - ddof))


def percentile(sorted_vals: Sequence[float], q: float) -> float:
    """线性插值分位数（q ∈ [0,100]）；空序列返回 0。"""
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * (q / 100.0)
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return float(sorted_vals[int(k)])
    return float(sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo))


def normal_cdf(x: float) -> float:
    """标准正态 CDF（误差函数）。"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def t_two_sided_p(t: float, df: int) -> float:
    """双尾 p 值（正态近似；小样本仅作参考，输出须标注）。"""
    if df <= 0:
        return 1.0
    z = abs(t)
    # 小样本用正态近似会低估尾部，这里保守乘一个有限样本修正系数
    penalty = 1.0 + (2.0 / max(df, 1))
    return min(1.0, 2.0 * (1.0 - normal_cdf(z * penalty)))


# ---------------------------------------------------------------------------
# 线性代数（高斯消元，部分主元）
# ---------------------------------------------------------------------------


def solve(A: Sequence[Sequence[float]], b: Sequence[float]) -> list[float]:
    """解线性方程组 A x = b；奇异时抛 ValueError。"""
    n = len(A)
    if n == 0 or any(len(row) != n for row in A) or len(b) != n:
        raise ValueError("solve: 维度不匹配")
    M = [list(A[i]) + [float(b[i])] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("solve: 矩阵奇异")
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(col + 1, n):
            f = M[r][col] / pv
            if f == 0.0:
                continue
            for c in range(col, n + 1):
                M[r][c] -= f * M[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = M[r][n] - sum(M[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / M[r][r]
    return x


def inverse(A: Sequence[Sequence[float]]) -> list[list[float]]:
    """矩阵求逆（逐列解 A x = e_i）；奇异时抛 ValueError。"""
    n = len(A)
    inv = [[0.0] * n for _ in range(n)]
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        col = solve(A, e)
        for i in range(n):
            inv[i][j] = col[i]
    return inv


# ---------------------------------------------------------------------------
# OLS
# ---------------------------------------------------------------------------


def ols(X: Sequence[Sequence[float]], y: Sequence[float]) -> dict:
    """普通最小二乘（含截距由调用方决定是否加入）。

    X: n×k 设计矩阵；y: n 维被解释变量。
    返回 dict：beta / fitted / resid / sigma2 / cov / se / t / p / r2 / n / k。
    p 值为正态近似（小样本仅作参考）。
    """
    n = len(y)
    if n == 0 or len(X) != n or any(len(row) != len(X[0]) for row in X):
        raise ValueError("ols: 维度不匹配")
    k = len(X[0])
    if n <= k:
        raise ValueError(f"ols: 样本不足（n={n}, k={k}）")
    XtX = [[sum(X[t][i] * X[t][j] for t in range(n)) for j in range(k)] for i in range(k)]
    Xty = [sum(X[t][i] * y[t] for t in range(n)) for i in range(k)]
    beta = solve(XtX, Xty)
    fitted = [sum(X[t][j] * beta[j] for j in range(k)) for t in range(n)]
    resid = [y[t] - fitted[t] for t in range(n)]
    ssr = sum(e * e for e in resid)
    sigma2 = ssr / (n - k)
    cov = [[sigma2 * v for v in row] for row in inverse(XtX)]
    se = [math.sqrt(max(cov[i][i], 0.0)) for i in range(k)]
    t = [beta[i] / se[i] if se[i] > 0 else 0.0 for i in range(k)]
    p = [t_two_sided_p(t[i], n - k) for i in range(k)]
    ybar = mean(y)
    sst = sum((v - ybar) ** 2 for v in y)
    r2 = 1.0 - ssr / sst if sst > 0 else 0.0
    return {
        "beta": beta,
        "fitted": fitted,
        "resid": resid,
        "sigma2": sigma2,
        "cov": cov,
        "se": se,
        "t": t,
        "p": p,
        "r2": r2,
        "n": n,
        "k": k,
    }


def with_intercept(x: Sequence[float]) -> list[list[float]]:
    """一元序列 → 带截距列的设计矩阵。"""
    return [[1.0, float(v)] for v in x]


# ---------------------------------------------------------------------------
# VAR（向量自回归，滞后可选手写实现）
# ---------------------------------------------------------------------------


def var_design(Y: Sequence[Sequence[float]], p: int) -> tuple[list[list[float]], list[list[float]]]:
    """把 T×m 多元序列转为 VAR(p) 的设计矩阵与目标矩阵。

    每行特征 = [1, y_{t-1}(m 个), y_{t-2}(m 个), …, y_{t-p}(m 个)]。
    """
    T = len(Y)
    if p < 1 or T <= p + 1:
        raise ValueError("var_design: 样本不足")
    Z, target = [], []
    for t in range(p, T):
        row = [1.0]
        for lag in range(1, p + 1):
            row.extend(float(v) for v in Y[t - lag])
        Z.append(row)
        target.append([float(v) for v in Y[t]])
    return Z, target


def var_fit(Y: Sequence[Sequence[float]], p: int) -> dict:
    """拟合 VAR(p)：对每个变量分别 OLS。

    返回 dict：m / p / coef（m 个方程，每个 k=1+m*p 系数）/ aic / bic / resid。
    """
    Z, target = var_design(Y, p)
    m = len(Y[0])
    coef, resid = [], []
    for j in range(m):
        yj = [row[j] for row in target]
        fit = ols(Z, yj)
        coef.append(fit["beta"])
        resid.append(fit["resid"])
    T = len(Z)
    k = len(Z[0])
    # 简化 AIC/BIC：用各方程残差平方和之和
    ssr = sum(sum(e * e for e in r) for r in resid)
    n_par = m * k
    aic = T * math.log(ssr / T) + 2 * n_par if ssr > 0 else float("-inf")
    bic = T * math.log(ssr / T) + math.log(T) * n_par if ssr > 0 else float("-inf")
    return {"m": m, "p": p, "coef": coef, "aic": aic, "bic": bic, "resid": resid, "n": T, "k": k}


def var_select_order(Y: Sequence[Sequence[float]], max_p: int = 4) -> int:
    """用 BIC 选择 VAR 滞后阶数（1..max_p）。"""
    best_p, best_bic = 1, float("inf")
    for p in range(1, max_p + 1):
        try:
            fit = var_fit(Y, p)
        except ValueError:
            break
        if fit["bic"] < best_bic:
            best_bic, best_p = fit["bic"], p
    return best_p


def var_irf(coef: Sequence[Sequence[float]], m: int, p: int, steps: int,
            shock_var: int = 0, shock_size: float = 1.0) -> list[list[float]]:
    """VAR 脉冲响应（Cholesky 未做正交化，采用递归代入）。

    coef: var_fit 的 coef；返回 steps×m 的响应矩阵（第 0 期为冲击当期）。
    """
    k = 1 + m * p
    if any(len(row) != k for row in coef):
        raise ValueError("var_irf: 系数维度与 m/p 不匹配")
    hist = [[0.0] * m for _ in range(p)]  # 前 p 期置于 0
    irf: list[list[float]] = []
    for _ in range(steps):
        row = [1.0]
        for lag in range(1, p + 1):
            row.extend(hist[-lag] if lag <= len(hist) else [0.0] * m)
        nxt = [sum(coef[j][i] * row[i] for i in range(k)) for j in range(m)]
        if len(irf) == 0:
            nxt[shock_var] += shock_size
        irf.append(nxt)
        hist.append(nxt)
    return irf


# ---------------------------------------------------------------------------
# 记录读取
# ---------------------------------------------------------------------------


def read_csv_records(path) -> list[dict]:
    """读取 CSV（utf-8-sig，含表头）→ 记录字典列表。"""
    import csv

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_float(v, default=0.0) -> float:
    """容错转 float；空/非法返回 default。"""
    try:
        if v is None or str(v).strip() == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default
