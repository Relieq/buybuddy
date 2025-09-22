# buybuddy
Trợ lý mua sắm dùng ADK + MCP + A2A + AP2

Mục tiêu học 4 công nghệ:
* ADK (Agent Development Kit): khung để dựng, chạy và triển khai agent (hướng Gemini nhưng model-agnostic).
* MCP (Model Context Protocol): “cổng USB-C” cho LLM kết nối sources & tools chuẩn hoá.
* A2A (Agent-to-Agent): chuẩn để các agent giao tiếp/hợp tác liên hệ công việc.
* AP2 (Agent Payments Protocol): chuẩn mới để agent thực hiện thanh toán an toàn với “mandate/ủy quyền” và đa phương thức 
(thẻ, chuyển khoản real-time, stablecoin…).

Bài toán & kiến trúc

Bài toán: người dùng nêu yêu cầu (“mua bàn phím cơ ≤ 2 triệu, giao nhanh”). BuyBuddy:
* Tìm & so sánh sản phẩm; 2) Chat với “VendorAgent” qua A2A để chốt hàng;
* Gọi MCP tools để truy cập kho dữ liệu (giá, tồn, giao hàng), logs, và các hành động (thêm vào giỏ, tạo đơn nháp);
* Khi thanh toán, thực hiện AP2 với “mandate” rõ ràng;
* Tất cả được dàn nhạc trong ADK (pipeline, state, retry, eval runbook).

Cấu trúc thư mục
```
buybuddy/
  apps/
    buyer_agent/
      __init__.py           
      main.py               # CLI app (entrypoint `buybuddy run`)
      agent_runtime.py      # lõi agent: state, messages, think/act/respond
      tools_local.py        # “tool” nội bộ: search sản phẩm từ catalog.json
      data/
        catalog.json        # dữ liệu mẫu về sản phẩm
  packages/
    contracts/
      __init__.py
      schemas/
        a2a_intents.json    # (placeholder) schema cho thông điệp A2A (sẽ dùng ở Stage 3)
        ap2_objects.json    # (placeholder) schema cho Mandate/Payment/Receipt (Stage 4)
        mcp_tools.json      # (placeholder) schema cho tool MCP (Stage 2/5)
  tests/
    __init__.py             # chỗ để viết test sau này
  pyproject.toml            # cấu hình gói, dep, script CLI
  README.md                 # hướng dẫn chạy nhanh
```

# BuyBuddy (Stage 1)

Goals:
* Vòng lặp CLI với runtime agent đơn giản có trạng thái
* Gọi công cụ cục bộ (tìm kiếm sản phẩm) từ danh mục JSON
* Các đường nối rõ ràng để sau này kết nối MCP, A2A và AP2

## Khởi tạo
* Tạo file `pyproject.toml` khai báo gói, dep, script CLI:
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "buybuddy"
version = "0.1.0"
description = "BuyBuddy — Shopping agent playground (ADK + MCP + A2A + AP2)"
authors = [{name = "Tên bạn"}]
readme = "README.md"
requires-python = ">=3.12"
dynamic = ["dependencies"]

[tool.setuptools.dynamic]
dependencies = {file = ["requirements.txt"]}

[project.scripts]
buybuddy = "apps.buyer_agent.main:app"

[tool.ruff]
line-length = 120

[tool.black]
line-length = 120
```
* Tạo file `requirements.txt` khai báo thư viện cần thiết như trong repo.
* Cài các thư viện:
```bash
pip install -e .
```
## Tạo BuyerAgent
* Tạo package `apps/buyer_agent/`
* Tạo file `apps/buyer_agent/agent_runtime.py`:
```python

```
