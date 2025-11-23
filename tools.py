from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
import yfinance as yf
import os

def fetch_price_data(ticker_symbol: str):
    ticker = yf.Ticker(ticker=ticker_symbol)
    historical_data = ticker.history(period="1mo")
    return {
        "current_price": ticker.info['currentPrice'],
        "market_cap": ticker.info['marketCap'],
        "pe_ratio": ticker.info.get('trailingPE', 'N/A'),
        "volume": ticker.info.get('volume'),
        "sector": ticker.info['sector'],
        "historical_data": historical_data
    }


async def fetch_news(ticker_symbol: str):
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-brave-search"],
        env={"BRAVE_API_KEY": os.environ["BRAVE_API_KEY"],
             **os.environ}
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            search_result = await session.call_tool(name="brave_news_search", arguments={"query": f"{ticker_symbol} stock news"})
            news_text = search_result.content[0].text
            return news_text
