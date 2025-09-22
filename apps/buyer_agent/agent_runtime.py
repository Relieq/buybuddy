from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Message:
    role: str # 'user', 'assistant', hoặc 'tool' (output của công cụ)
    content: str
    name: str | None = None # Định danh cụ thể, ví dụ: BuyerAgent, VendorAgent, search_products, v.v.

@dataclass
class AgentState:
    messages: List[Message] = field(default_factory=list)
    budget_vnd: int = 2_000_000 # budget mặc định cho demo
    brand_caps: List[str] = field(default_factory=list)

class BuyerAgent:
    def __init__(self):
        self.state = AgentState()

    def observe(self, role: str, content: str, name: str | None = None):
        self.state.messages.append(Message(role=role, content=content, name=name))

    def think(self, prompt: str) -> str:
        # Stage-1: heuristic "thinking" (no LLM yet)
        lower = prompt.lower()
        if "ban phim" in lower or "keyboard" in lower:
            return "Search for mechanical keyboards under budget and summarize top options."
        return "Search for products related to the query under budget and summarize."

    def act_tool(self, tool_call: Dict[str, any], tool_fn) -> Dict[str, any]:
        result = tool_fn(**tool_call.get("args", {})) # dictionary unpacking
        # Giả sử bạn có một dict như args = {"a": 1, "b": 2}, thì func(**args) tương đương với func(a=1, b=2).
        self.observe("tool", str(result), tool_call.get("name"))
        return result

    def response(self, observation: Dict[str, any]) -> str:
        if not observation or "items" not in observation:
            return "Mình chưa tìm thấy gì phù hợp. Bạn có thể mô tả rõ hơn nhu cầu không?"
        items = observation["items"][:3]
        summary_lines = [
            f"- {it['name']} — {it['price']}₫ | ship ~{it['eta']} | id={it['id']}"
            for it in items
        ]
        return "Mình gợi ý 3 lựa chọn đầu tiên:\n" + "\n".join(summary_lines)
