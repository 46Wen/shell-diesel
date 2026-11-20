# 顺路最便宜的 Shell 柴油

手机网页：输入目的地，列出路线附近最划算的 Shell 加油站（不含 Shell Express），可以切换 Diésel normal / Diésel premium。

每个加油站显示：
- 每升价格、营业时间、地址；
- 从出发地开到站的真实路线距离和时间；
- 绕路多出多少公里和分钟；
- 加满要多少钱（按你选的剩余油量和油箱容量计算）；
- 实际总花费（加满 + 绕路多耗的油费），并按它排名；
- "复制地址"和"在 Waze 打开"按钮。

## 数据来源

- 油价：西班牙工业部 Geoportal de Gasolineras 开放数据（官方牌价，不含 ClubSmart 折扣）。
  `.github/workflows/update.yml` 每小时运行 `scripts/update.py`，只保留 Shell 加油站，存到 `data/shell.json`。
- 地址搜索：OpenStreetMap Nominatim。
- 路线、距离、时间：OSRM 公共路线服务。

## 托管

GitHub Pages：Settings → Pages → Source 选 "Deploy from a branch"，分支选 `main`，目录选 `/ (root)`。
网址是 `https://<用户名>.github.io/shell-diesel/`。在 iPhone Safari 打开后，点"分享"→"添加到主屏幕"。
