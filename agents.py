from crewai import Agent
from textwrap import dedent
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import ExtractionTools, DataFetchingTools, ChartingTools, MarkdownTools
from dotenv import load_dotenv
import os

load_dotenv() 

oai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

class FinancialResearchAgents:
    def __init__(self):
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.4, api_key=oai_api_key)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.5)
        # self.Ollama = Ollama(model="openhermes")
        self.gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                                verbose=True, temperature=0.5, google_api_key=gemini_api_key)

    def markdown_report_creator(self):
        return Agent(
            role="Markdown 報告創建者",
            goal=dedent(f"""為特定的符號檢索所請求的指標的準確數據。"""),
            backstory=dedent(f"""專門創建 markdown 報告。最擅長使用工具從 API 中收集數據。當被問到時，你從 QuickFS 檢索**每一個**指標，並且從不錯過任何一個。"""),
            tools=[
                ExtractionTools.parse_string, 
                DataFetchingTools.get_metric_data_from_quickfs],
            verbose=True,
            llm=self.gemini,
        )

    def chart_creator(self):
        return Agent(
            role="圖表創建者",
            goal=dedent(f"""使用提供的工具創建數據的圖表。"""),
            backstory=dedent(f"""專門創建圖表。你以接收一系列數據點並精確地創建圖表而聞名。你必須使用提供的工具。"""),
            tools=[
                ChartingTools.create_chart
            ] ,
            verbose=True,
            llm=self.gemini,
        )

    
    def markdown_writer(self):
        return Agent(
            role="數據報告創建者",
            goal=dedent(f"""使用同一目錄下的 *.png 檔案，添加正確的 markdown 檔案語法。"""),
            backstory=dedent(f"""專門在 markdown 檔案中寫入文字。你接收文字輸入並將內容寫入同一目錄下的 markdown 檔案。在插入 markdown 檔案後，你總是添加新的一行。**無論何時你都使用 MARKDOWN 語法** 你從不在 report.md 檔案中插入任何非 MARKDOWN 語法的內容。"""),
            tools=[MarkdownTools.write_text_to_markdown_file],
            verbose=True,
            llm=self.gemini,
        )



     