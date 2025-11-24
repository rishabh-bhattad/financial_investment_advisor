from state import AdvisorState
from tools import fetch_news, fetch_price_data
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    google_api_key=os.environ['GOOGLE_API_KEY']
)


def market_data_node(state: AdvisorState):
    ticker = state['ticker']
    return {'price_data': fetch_price_data(ticker_symbol=ticker)}


async def research_node(state: AdvisorState):
    ticker = state['ticker']
    return {'news_data': await fetch_news(ticker_symbol=ticker)}


def analyst_node(state: AdvisorState):
    ticker = state['ticker']
    price_data = state['price_data']
    news_data = state['news_data']
    news_string = "\n".join(news_data)
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a financial analyst. Analyze the provided technical data and news sentiment to determine a Buy/Sell/Hold rating."),
            ("human", "Ticker: {ticker}\n\nFinancial Data: {prices}\n\nNews Summary: {news}")
        ]
    )

    chain = template | llm
    response = chain.invoke({
        "ticker": ticker,
        "prices": price_data,
        "news": news_string
    })

    return {'analyst_reasoning': response.content}
    