from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from difflib import get_close_matches

app = FastAPI()

# 策略库（全小写 key）
strategy_library = {
    "macd金叉": "MACD金叉触发买点",
    "ma多头排列": "均线多头排列触发买点",
    "kdj金叉": "KDJ指标金叉",
    "macd死叉": "MACD死叉触发卖点",
    "ma空头排列": "均线空头排列触发卖点",
    # 可扩展其他条件...
}

class StrategyInput(BaseModel):
    buyConditions: List[str]
    sellConditions: List[str]

def find_similar(condition: str, lib_keys: List[str], cutoff=0.6) -> List[str]:
    return get_close_matches(condition, lib_keys, n=1, cutoff=cutoff)

@app.post("/运行回测")
async def run_strategy(data: StrategyInput):
    buy_conditions = [c.strip().lower() for c in data.buyConditions]
    sell_conditions = [c.strip().lower() for c in data.sellConditions]
    lib_keys = list(strategy_library.keys())

    matched_buy = []
    unmatched_buy: Dict[str, List[str]] = {}

    for cond in buy_conditions:
        if cond in strategy_library:
            matched_buy.append(strategy_library[cond])
        else:
            similar = find_similar(cond, lib_keys)
            unmatched_buy[cond] = similar

    matched_sell = []
    unmatched_sell: Dict[str, List[str]] = {}

    for cond in sell_conditions:
        if cond in strategy_library:
            matched_sell.append(strategy_library[cond])
        else:
            similar = find_similar(cond, lib_keys)
            unmatched_sell[cond] = similar

    return {
        "解释": explanation,
        "已识别买入策略": matched_buy,
        "已识别卖出策略": matched_sell,
        "未识别买入条件及推荐": unmatched_buy,
        "未识别卖出条件及推荐": unmatched_sell
    }


def explain_conditions(buy_conditions, sell_conditions):
    explanation = []

    def explain_single_condition(cond):
        if "30日均线高于5/10/20日均线" in cond:
            return "当前为多头排列（30日线高于5/10/20日线），短期趋势向上"
        if "MACD金叉" in cond:
            return "MACD出现金叉，趋势可能反转向上"
        if "涨幅达到30%" in cond:
            return "涨幅达到30%时止盈，建议设置提醒"
        if "最大回撤超过20%" in cond:
            return "若最大回撤超20%则止损，防守策略"
        return cond  # 默认直接返回原文

    if buy_conditions:
        buy_text = "✅ 已识别买入条件：" + "，".join(explain_single_condition(c) for c in buy_conditions)
        explanation.append(buy_text)

    if sell_conditions:
        sell_text = "✅ 已识别卖出条件：" + "，".join(explain_single_condition(c) for c in sell_conditions)
        explanation.append(sell_text)

    if buy_conditions and sell_conditions:
        explanation.append("📊 推荐策略：中短线趋势策略，建议持有周期约1–2个月。")

    return " ".join(explanation)
