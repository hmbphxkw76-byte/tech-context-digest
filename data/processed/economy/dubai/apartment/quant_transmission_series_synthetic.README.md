# 传导弹性示意序列（SYNTHETIC，非真实数据）

`quant_transmission_series_synthetic.csv` 是为验证 `engine/tools/transmission.py` 的
OLS/VAR 接口而构造的**结构性示意序列**，**不是真实市场数据**，不得作为研究结论引用。

- 用途：模块自检、CI 数值用例、接口演示。
- 处置：待第 2 章 11 维数据项取得官方一手序列后，替换为 `quant_transmission_series.csv`
  并删除本示意文件。
- 口径：列名沿用 `transmission.CHAINS`（EIBOR_3M / VOLUME_YOY / COMPLETIONS_YOY /
  RENT_YOY / FDI_YOY / PRICE_YOY / SEARCH_INDEX）。
