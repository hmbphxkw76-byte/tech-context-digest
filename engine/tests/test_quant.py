"""量化研究体系模块单元测试（实施方案落地校验）。

覆盖：_quant 线性代数/计量、cycle_clock、signal_synth、policy_multiplier、
transmission（OLS/VAR）、valuation、market_sizing、stress_test、monte_carlo、
threshold_calibration、research_kernel_check。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import _quant  # noqa: E402
import cycle_clock  # noqa: E402
import market_sizing  # noqa: E402
import monte_carlo  # noqa: E402
import policy_multiplier  # noqa: E402
import research_kernel_check  # noqa: E402
import signal_synth  # noqa: E402
import stress_test  # noqa: E402
import threshold_calibration  # noqa: E402
import transmission  # noqa: E402
import valuation  # noqa: E402


class TestQuantLA(unittest.TestCase):
    def test_solve(self):
        x = _quant.solve([[2.0, 1.0], [1.0, 3.0]], [5.0, 10.0])
        self.assertAlmostEqual(x[0], 1.0, places=6)
        self.assertAlmostEqual(x[1], 3.0, places=6)

    def test_inverse(self):
        A = [[2.0, 1.0], [1.0, 3.0]]
        inv = _quant.inverse(A)
        self.assertAlmostEqual(inv[0][0], 0.6, places=6)
        self.assertAlmostEqual(inv[1][1], 0.4, places=6)

    def test_ols_recovers_beta(self):
        x = [float(i) for i in range(20)]
        y = [3.0 + 2.0 * v for v in x]
        fit = _quant.ols(_quant.with_intercept(x), y)
        self.assertAlmostEqual(fit["beta"][1], 2.0, places=6)
        self.assertAlmostEqual(fit["beta"][0], 3.0, places=6)
        self.assertAlmostEqual(fit["r2"], 1.0, places=6)

    def test_percentile(self):
        self.assertEqual(_quant.percentile([1.0, 2.0, 3.0, 4.0], 50), 2.5)
        self.assertEqual(_quant.percentile([], 50), 0.0)

    def test_var_irf_shape(self):
        Y = [[float(i % 5), float((i * 2) % 7)] for i in range(12)]
        p = _quant.var_select_order(Y, 3)
        fit = _quant.var_fit(Y, p)
        irf = _quant.var_irf(fit["coef"], fit["m"], p, steps=5)
        self.assertEqual(len(irf), 5)
        self.assertEqual(len(irf[0]), 2)


class TestCycleClock(unittest.TestCase):
    @staticmethod
    def _records(indicators: dict) -> list[dict]:
        recs = []
        for ind, vals in indicators.items():
            for i, v in enumerate(vals):
                recs.append({"indicator": ind, "date": f"2026-{(i + 1):02d}-01", "value": v})
        return recs

    def test_overheat(self):
        recs = self._records({"GDP_YOY": [4.0, 4.2, 4.5, 4.8], "CPI_YOY": [2.0, 2.4, 2.8, 3.0],
                              "POLICY_RATE": [0, 0, 0, 0], "M2_GROWTH": [6, 6, 6, 6]})
        self.assertEqual(cycle_clock.classify(recs).phase, "过热")

    def test_transition(self):
        recs = self._records({"GDP_YOY": [4.0, 4.2, 4.5, 4.8], "CPI_YOY": [2.0, 2.4, 2.8, 3.0],
                              "POLICY_RATE": [0, 0.4, 0.9, 1.5]})
        self.assertEqual(cycle_clock.classify(recs).phase, "过渡带")

    def test_stagflation(self):
        recs = self._records({"GDP_YOY": [3.0, 2.0, 1.5, 1.0], "CPI_YOY": [2.0, 2.4, 2.8, 3.0]})
        self.assertEqual(cycle_clock.classify(recs).phase, "滞胀")

    def test_recovery(self):
        recs = self._records({"GDP_YOY": [3.0, 3.2, 3.5, 4.0], "CPI_YOY": [1.5, 1.2, 0.8, 0.5]})
        self.assertEqual(cycle_clock.classify(recs).phase, "复苏")

    def test_recession(self):
        recs = self._records({"GDP_YOY": [2.0, 1.5, 1.0, 0.5], "CPI_YOY": [1.5, 1.0, 0.5, 0.2]})
        self.assertEqual(cycle_clock.classify(recs).phase, "衰退")

    def test_deterministic(self):
        recs = self._records({"GDP_YOY": [4.0, 4.2, 4.5, 4.8], "CPI_YOY": [2.0, 2.4, 2.8, 3.0]})
        a = cycle_clock.classify(recs).to_dict()
        b = cycle_clock.classify(recs).to_dict()
        self.assertEqual(a, b)


class TestSignalSynth(unittest.TestCase):
    def test_all_green(self):
        st = {k: "绿" for k in signal_synth.K_META}
        r = signal_synth.synthesize(st)
        self.assertEqual(r.overall_score, 0.0)
        self.assertEqual(r.consistency, "高")

    def test_layer_weights_sum(self):
        self.assertAlmostEqual(sum(signal_synth.LAYER_WEIGHT.values()), 1.0, places=6)
        self.assertEqual(len([k for k, v in signal_synth.K_META.items() if v[0] == "领先"]), 8)
        self.assertEqual(len([k for k, v in signal_synth.K_META.items() if v[0] == "同步"]), 5)
        self.assertEqual(len([k for k, v in signal_synth.K_META.items() if v[0] == "滞后"]), 2)

    def test_phase_conflict(self):
        st = {k: "硬红·完全" for k in signal_synth.K_META}
        r = signal_synth.synthesize(st, phase="复苏")
        self.assertTrue(r.phase_conflict)
        self.assertEqual(r.consistency, "高")


class TestPolicyMultiplier(unittest.TestCase):
    def test_load_default(self):
        pols = policy_multiplier.load()
        self.assertEqual(len(pols), 5)
        v, t, rate = policy_multiplier.coverage(pols)
        self.assertEqual((v, t), (1, 5))
        self.assertAlmostEqual(rate, 0.2, places=6)

    def test_unverified_has_no_multiplier(self):
        for p in policy_multiplier.load():
            if p.status != policy_multiplier.VERIFIED:
                self.assertIsNone(p.multiplier_low)
                self.assertIsNone(p.multiplier_high)

    def test_validate_rejects_unverified_multiplier(self):
        p = policy_multiplier.Policy(id="X", name="x", tool="t", chain="c",
                                     lag_quarters="1", status="未核验")
        p.multiplier_low = -1.0
        with self.assertRaises(ValueError):
            policy_multiplier.validate_policy(p)


class TestTransmission(unittest.TestCase):
    def test_ols_elasticity(self):
        x = [float(i % 7) for i in range(40)]
        y = [100.0 + 10.0 * v for v in x]
        e = transmission.estimate_ols(y, x, chain="rate")
        self.assertIsNotNone(e.eta)
        self.assertGreater(e.r2, 0.9)
        self.assertGreaterEqual(e.lag, 0)

    def test_ols_short_sample(self):
        e = transmission.estimate_ols([1, 2, 3], [1, 2, 3], chain="rate")
        self.assertIsNone(e.eta)

    def test_var_elasticity_shape(self):
        series = {"A": [float(i % 5) for i in range(20)],
                  "B": [float((i * 3) % 8) for i in range(20)]}
        e = transmission.estimate_var(series, chain="rate")
        self.assertEqual(e.method, "VAR")

    def test_chain_spec(self):
        self.assertEqual(set(transmission.CHAINS), {"rate", "supply", "demand", "sentiment"})


class TestValuation(unittest.TestCase):
    def test_cap_rate(self):
        r = valuation.cap_rate(60000, 1000000, {"物业费": 6000})
        self.assertAlmostEqual(r.gross_cap, 0.06, places=6)
        self.assertAlmostEqual(r.net_cap, 0.054, places=6)

    def test_dcf(self):
        r = valuation.dcf([50000, 52000, 54000], [0.044, 0.044, 0.044], terminal_value=1000000)
        self.assertGreater(r.npv, 0)
        self.assertEqual(len(r.pv_periods), 3)

    def test_sensitivity_monotonic(self):
        base = valuation.sensitivity_cap(60000, 1000000, rate_shock_bp=0)["stressed_net_cap"]
        up = valuation.sensitivity_cap(60000, 1000000, rate_shock_bp=50)["stressed_net_cap"]
        self.assertGreater(up, base)

    def test_relative(self):
        r = valuation.relative_valuation(0.054, 0.0436, 0.055)
        self.assertAlmostEqual(r["premium_to_risk_free_pp"], 1.04, places=2)


class TestMarketSizing(unittest.TestCase):
    def test_top_down(self):
        r = market_sizing.top_down(1000.0, 0.5, 0.2)
        self.assertEqual((r.tam, r.sam, r.som), (1000.0, 500.0, 100.0))

    def test_bottom_up(self):
        r = market_sizing.bottom_up(100, 10, 0.5, 0.2)
        self.assertEqual(r.tam, 1000.0)
        self.assertEqual(r.som, 100.0)

    def test_constraint_violation(self):
        with self.assertRaises(ValueError):
            market_sizing.bottom_up(100, 10, sam_share=1.5)

    def test_compare_gap(self):
        top = market_sizing.top_down(1000.0, 0.5, 0.2)
        bot = market_sizing.bottom_up(100, 10)
        c = market_sizing.compare(top, bot)
        self.assertTrue(c["within_30pct"])


class TestStressTest(unittest.TestCase):
    def test_run_all(self):
        results = stress_test.run_all()
        self.assertGreaterEqual(len(results), 5)
        for r in results:
            self.assertTrue(r.trigger)
            self.assertIsInstance(r.impacts, dict)

    def test_scenario_impact_sign(self):
        s = {"id": "T", "name": "t", "trigger": "x", "shocks": {"demand_to_price": -4.0}}
        r = stress_test.run_scenario(s)
        self.assertEqual(r.impacts.get("PRICE_YOY"), -2.4)


class TestMonteCarlo(unittest.TestCase):
    def test_deterministic(self):
        d = {"a": (0.0, 1.0)}
        r1 = monte_carlo.simulate(d, [("a", -0.8)], n=1000, seed=42)
        r2 = monte_carlo.simulate(d, [("a", -0.8)], n=1000, seed=42)
        self.assertEqual(r1.to_dict(), r2.to_dict())

    def test_percentile_order(self):
        r = monte_carlo.simulate({"a": (0.0, 1.0)}, [("a", 1.0)], n=5000, seed=7)
        self.assertLessEqual(r.percentiles["P10"], r.percentiles["P50"])
        self.assertLessEqual(r.percentiles["P50"], r.percentiles["P90"])
        self.assertLessEqual(r.var_95, r.percentiles["P10"])


class TestThresholdCalibration(unittest.TestCase):
    def test_calibrate(self):
        cal = threshold_calibration.calibrate([float(i) for i in range(100)], window=36)
        self.assertLess(cal.low, cal.high)
        self.assertEqual(cal.n, 36)

    def test_state_count(self):
        s = [0, 1, 2, 3, 2, 1, 0]
        ep = threshold_calibration.state_count(s, 2)
        self.assertEqual(len(ep), 1)
        self.assertEqual(ep[0]["duration"], 3)

    def test_trigger_count(self):
        self.assertEqual(threshold_calibration.trigger_count([0, 1, 2, 3], 2), 2)

    def test_backtest(self):
        b = threshold_calibration.backtest([1, -1, 1], [2, -2, 3])
        self.assertEqual(b["hit_rate"], 1.0)


class TestResearchKernelCheck(unittest.TestCase):
    def test_check_text_complete(self):
        t = "周期定位 周期阶段；弹性 时滞；政策乘数 入模；未核验 盲区"
        self.assertEqual(research_kernel_check.check_text(t), [])

    def test_check_text_missing(self):
        self.assertEqual(research_kernel_check.check_text("无内容"),
                         ["周期定位", "传导量化", "政策入模", "盲区列示"])

    def test_period_gate(self):
        self.assertEqual(research_kernel_check._period_of("2026-11_monthly.html"), "2026-11")
        self.assertEqual(research_kernel_check._period_of("2026-11-13_weekly.html"), "2026-11-13")
        self.assertEqual(research_kernel_check._period_of("foo.html"), "")

    def test_period_key_compare(self):
        k = research_kernel_check._period_key
        self.assertGreaterEqual(k("2026-12"), k("2026-12"))
        self.assertLess(k("2026-Q3"), k("2026-12"))
        self.assertLess(k("2026-11-13"), k("2026-12"))
        self.assertGreaterEqual(k("2026-12-01"), k("2026-12"))


if __name__ == "__main__":
    unittest.main()
