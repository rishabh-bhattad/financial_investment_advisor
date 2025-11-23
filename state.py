from typing import TypedDict, Optional, List

class AdvisorState(TypedDict):
    ticker: Optional[str]
    price_data: Optional[str]
    news_data: Optional[List[str]]
    analyst_reasoning: Optional[str]
    final_report: Optional[str]
    revision_number: Optional[int]