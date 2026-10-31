# PVC 均价线交易系统 API 文档

## 基础信息

- **Base URL**: `http://localhost:8080/api/v1`
- **Content-Type**: `application/json`

## 端点列表

### 健康检查

```
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2026-10-30T12:00:00+08:00",
  "version": "1.0.0"
}
```

### 获取当前持仓

```
GET /positions
```

**响应示例**:
```json
{
  "positions": [
    {
      "symbol": "pvc2401",
      "direction": "long",
      "quantity": 10,
      "entry_price": 5023.5,
      "stop_loss": 4923.0,
      "take_profit": 5223.5,
      "entry_time": "2026-10-30T10:30:00+08:00"
    }
  ]
}
```

### 下单

```
POST /orders
```

**请求体**:
```json
{
  "symbol": "pvc2401",
  "direction": "long",
  "quantity": 10,
  "order_type": "market",
  "price": null,
  "stop_loss": 4923.0,
  "take_profit": 5223.5
}
```

**响应示例**:
```json
{
  "order_id": "ORD20261030123456",
  "status": "submitted",
  "timestamp": "2026-10-30T12:00:00+08:00"
}
```

### 查询交易历史

```
GET /trades?symbol=pvc2401&limit=50
```

**响应示例**:
```json
{
  "trades": [
    {
      "trade_id": "TRD20261030123456",
      "symbol": "pvc2401",
      "direction": "long",
      "quantity": 10,
      "entry_price": 5023.5,
      "exit_price": 5050.0,
      "pnl": 265.0,
      "entry_time": "2026-10-30T10:30:00+08:00",
      "exit_time": "2026-10-30T11:45:00+08:00"
    }
  ],
  "total": 1
}
```

### 获取性能指标

```
GET /metrics
```

**响应示例**:
```json
{
  "uptime": "99.5%",
  "total_trades": 156,
  "win_rate": "62%",
  "max_drawdown": "8.2%",
  "sharpe_ratio": 1.35,
  "total_pnl": 12450.50,
  "daily_pnl": 342.00
}
```

### 获取系统状态

```
GET /status
```

**响应示例**:
```json
{
  "engine": "running",
  "symbols": ["pvc2401", "pvc2405"],
  "lease_status": {
    "current_active": "http://primary-server:8080",
    "primary_alive": true,
    "backup_alive": true
  },
  "daily_pnl": 342.00
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 认证

所有API请求需要在Header中携带API Key：

```
Authorization: Bearer YOUR_API_KEY
```

## 注意事项

1. 所有价格单位为元（CNY）
2. 时间格式为ISO 8601
3. 交易时间为交易时段（期货）或交易时段（股票）
4. 部分接口需要管理员权限
