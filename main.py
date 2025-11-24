from langgraph.graph import START, END, StateGraph
from state import AdvisorState
from nodes import analyst_node, research_node, market_data_node, writer_node
import asyncio


async def main():
    ticker = "AAPL"
    workflow = StateGraph(AdvisorState)
    workflow.add_node("market", market_data_node)
    workflow.add_node("news", research_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)

    workflow.add_edge(START, "market")
    workflow.add_edge(START, "news")
    workflow.add_edge("market", "analyst")
    workflow.add_edge("news", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", END)

    app = workflow.compile()
    result = await app.ainvoke({"ticker": ticker})
    print(result['final_report'])


if __name__ == "__main__":
    asyncio.run(main())
