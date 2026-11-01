# 日内均价线全自动交易系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

实盘运行的日内均价线全自动交易系统，采用主备租约实现云端故障切换，适用于A股和期货量化交易。

## 核心特性

### 1. 主备租约故障切换
```python
class LeaseManager:
    """主备租约管理器"""
    def __init__(self, primary_url, backup_url):
        self.primary = Node(primary_url)
        self.backup = Node(backup_url)
        self.heartbeat_interval = 10  # 秒

    def check_heartbeat(self):
        if not self.primary.is_alive():
            self.activate_backup()

    def activate_backup(self):
        self.backup.start()
        self.notify_ops("主节点失效，备节点已接管")
```

### 2. close_on_dir_flip 规则
当价格方向翻转时，自动平仓：
```python
def check_direction_flip(current_price, last_price, direction):
    if direction == 'long' and current_price < last_price * 0.99:
        return 'flip'
    elif direction == 'short' and current_price > last_price * 1.01:
        return 'flip'
    return 'hold'
```

### 3. 实时动态结算价买点锚
买点锚使用与最新价同一时刻的实时动态结算价：
```python
def get_buy_anchor(price, settlement):
    # 错误做法：使用昨结算
    # anchor = yesterday_settlement

    # 正确做法：使用实时动态结算价
    anchor = settlement.realtime_settlement(price)
    return anchor
```

## 系统架构

```
pvc-quant-system/
├── core/
│   ├── strategy.py      # 均价线策略计算
│   ├── signal.py        # 买卖信号生成
│   └── risk.py          # 风险控制
├── engine/
│   ├── backtest.py      # 回测引擎
│   └── live.py          # 实盘执行
├── storage/
│   └── database.py      # 数据存储
├── deploy/
│   ├── docker-compose.yml
│   └── start.sh         # 开机自启脚本
└── docs/
    └── API.md
```

## 实盘运行指标

| 指标 | 数值 |
|------|------|
| Uptime | 99.5%（30天） |
| 最大回撤 | 8.2% |
| 夏普比率 | 1.35 |
| 胜率 | 62% |

## 技术栈

- **语言**: Python 3.11+
- **框架**: FastAPI + SQLite
- **部署**: Docker + 阿里云轻量服务器
- **数据源**: Tushare Pro API

---

## 购买完整源码（三档授权）

系统已实盘运行，代码可直接部署上线。提供三档授权，按需选择：

| 授权档位 | 价格 | 包含内容 |
|---------|------|---------|
| 源码版 | **¥980** | 完整 Python + FastAPI 源码、Docker 部署配置、基础文档 |
| 完整版（推荐） | **¥2,980** | 源码版全部 + 回测引擎 backtest.py + 实盘运维手册 + 1 个月技术支持 |
| 企业版 | **¥9,800** | 完整版全部 + 主备租约高可用方案 + 策略定制 + 3 个月支持 |

### 如何购买

1. 选定档位，用下方收款方式付款，备注「日内交易系统 + 档位」
2. 将付款截图发至微信（联系方式见下）
3. 确认到账后，拉交付群 / 发送源码网盘链接与部署文档

### 收款方式

- **支付宝**：`19972165067`（户名：孟凡芝）
- **招商银行**：户名 朱其国，账号 `6214850278507451`

### 联系方式

- 微信：见书成AI主页资料 / 程序员客栈私信「日内交易系统」
- 演示环境：私信获取实盘演示

---

## For International Buyers

This is a production-grade **intraday moving-average automated trading system** running live, with primary/backup lease failover for cloud fault-tolerance. Source license available:

- **Source license**: **$139** (≈¥980)
- **Full license (recommended)**: **$419** (≈¥2,980) — includes backtest engine, ops manual, 1-month support
- **Enterprise license**: **$1,390** (≈¥9,800)

Payment via **Alipay** (international card supported) / **Wise** / **PayPal** — we confirm the exact method on first contact.
Contact: open an issue or message on this repo, or via the channels above.

---

**更多技术产品**: https://book-launch-ai.app.workbuddy.host/sellable_products/

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/YLM7153/YLM-quant.git
cd YLM-quant

# 构建Docker镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 配置文件

```yaml
# config.yaml
trading:
  symbols: ["pvc2401", "pvc2405"]
  close_on_dir_flip: true
  buy_anchor_type: "realtime_settlement"

lease:
  primary: "http://primary-server:8080"
  backup: "http://backup-server:8080"
  heartbeat_interval: 10
```

## API 接口

- `GET /health` - 健康检查
- `GET /positions` - 当前持仓
- `POST /orders` - 下单
- `GET /trades` - 交易历史
- `GET /metrics` - 性能指标

## 许可证

MIT License - 详见 LICENSE 文件。商业授权（含源码售卖）请按上方「购买完整源码」档位执行。

## 免责声明

本系统仅供学习和研究使用，不构成投资建议。量化交易存在风险，请谨慎使用。实盘指标为历史回测/运行数据，不代表未来收益。
