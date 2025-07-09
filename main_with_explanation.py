from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

# 初始化 FastAPI
app = FastAPI()

# 允许跨域（确保前端本地调试时能访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class StrategyRequest(BaseModel):
    buyConditions: List[str]
    sellConditions: List[str]

# 通俗易懂的策略词典
strategy_library = {
    "macd金叉": "📈【MACD金叉】说明当前上涨力量增强，常用于观察买入时机。",
    "macd死叉": "⚠️【MACD死叉】可能是市场转弱信号，需注意风险。",
    "kdj死叉": "⚠️【KDJ死叉】可能是短线回落信号，请根据实际走势灵活判断。",
    "kdj金叉": "📈【KDJ金叉】短期资金介入迹象，可观察是否持续放量。",
    "ma多头排列": "📊【均线多头排列】表示短期、中期、长期趋势一致向上，市场整体偏强。",
    "成交量放大": "🔍【成交量放大】市场活跃度提高，通常伴随趋势加速。",
    "macd背离": "⚠️【MACD背离】价格与指标走势不同步，需谨防反转。",
    "均线拐头向上": "📈【均线拐头向上】均线方向开始上行，可能是趋势转强的初期信号。",
}

@app.post("/运行回测")
def run_strategy(strategy: StrategyRequest):
    buy_explanations = [
        strategy_library.get(item.lower(), f"📌 无法识别“{item}”，请检查拼写或换个说法")
        for item in strategy.buyConditions
    ]
    sell_explanations = [
        strategy_library.get(item.lower(), f"📌 无法识别“{item}”，请检查拼写或换个说法")
        for item in strategy.sellConditions
    ]
    return {
        "买入建议": buy_explanations,
        "卖出提醒": sell_explanations
    }
