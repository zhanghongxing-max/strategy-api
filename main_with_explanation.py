
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from difflib import get_close_matches

app = FastAPI(title="策略识别助手", description="帮股民快速理解你输入的买卖策略关键词", version="1.0")

# 简单的策略解释库
strategy_library = {
    "macd金叉": "MACD金叉通常表示买入信号",
    "ma多头排列": "均线多头排列说明趋势向上，考虑买入",
    "kdj金叉": "KDJ指标出现金叉，也可能是买入信号",
    "macd死叉": "MACD死叉可能是卖出信号",
    "ma死叉": "均线死叉说明趋势走弱，考虑卖出",
    "kdj死叉": "KDJ死叉通常是卖出提示"
}

class StrategyInput(BaseModel):
    buyConditions: List[str]
    sellConditions: List[str]

@app.post("/运行回测")
def run_strategy(input: StrategyInput):
    buy_explanations = []
    sell_explanations = []

    # 分析买入条件
    for cond in input.buyConditions:
        matched = get_close_matches(cond.lower(), strategy_library.keys(), n=1, cutoff=0.6)
        if matched:
            buy_explanations.append(strategy_library[matched[0]])
        else:
            buy_explanations.append(f"无法识别 '{cond}'，请检查拼写")

    # 分析卖出条件
    for cond in input.sellConditions:
        matched = get_close_matches(cond.lower(), strategy_library.keys(), n=1, cutoff=0.6)
        if matched:
            sell_explanations.append(strategy_library[matched[0]])
        else:
            sell_explanations.append(f"无法识别 '{cond}'，请检查拼写")

    return {
        "✅ 买入建议": buy_explanations,
        "🚫 卖出建议": sell_explanations
    }
