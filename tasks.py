from crewai import Task
from textwrap import dedent
from typing import List
from pydantic import BaseModel

class MarkdownReportCreationTasks:
    def __tip_section(self):
        return "如果你做出你的最好成果並且完全按照我所要求的回報，我將給你一萬美元的佣金！"

    def parse_input(self, agent, data: str):
        return Task(
               description=dedent(f"""
            **任務**：從字串中提取相關數據。
            **描述**：從輸入字串中獲取公司符號，並獲取任何可用的指標，除專用名詞或縮寫外，其餘盡量使用繁體中文。

            **參數**： 
            - 數據: {data}

            **備註**
            {self.__tip_section()}
            """
        ),
            agent=agent,
            expected_output="""一個包含符號和指標的字典列表。
            範例輸出：`[{'symbol': 'MSTR', 'metric': 'cogs'}, {'symbol': 'MSTR', 'metric': 'fcf'}]`"""
        )

    def get_data_from_api(self, agent, context):
        return Task(
               description=dedent(f"""
            **描述**：對於每個指標，使用工具查找由符號提供的指標，除專用名詞或縮寫外，其餘盡量使用繁體中文。

            **備註**
            你必須使用 QuickFS 獲取客戶請求的每個指標的數據。你可能需要多次完成此任務。
            {self.__tip_section()}
            """
        ),
            agent=agent,
            context=context,
            expected_output="""一個包含每個指標及其檢索到的數據的列表。
            範例輸出：[
                {metric:'fcf', data: [...data_points],
                {metric:'cogs', data: [...data_points],
                {...}
                ]"""
        )

    def create_charts(self, agent, context) -> Task:
        return Task(
            description=dedent(f"""
                創建代表公司財務指標的數據圖表。創建圖表的標題時，不要更改指標名稱，除專用名詞或縮寫外，其餘盡量使用繁體中文。

                {self.__tip_section()}
            """),
            agent=agent,
            context=context,
            expected_output="""
                創建的圖表的檔案位置列表。
                範例輸出：[fcf_chart.png, cogs_chart.png]
                """
        )


    def write_markdown(self, agent, context):
        return Task(
            description=dedent(f"""
                **任務**：將 markdown 語法插入 md 檔案
                **描述**：取得輸入的檔案位置並將其插入到 markdown 檔案中，除專用名詞或縮寫外，其餘盡量使用繁體中文。
                例如：將 ![](fcf_chart.png) 寫入到 markdown 檔案。

                你必須始終使用 MARKDOWN 語法。

                **備註**
                {self.__tip_section()}
            """
        ),
            agent=agent,
            expected_output="""一個以 markdown 語法格式化的 report.md 檔案。
            範例輸出： 
                ![](./COGS_chart.png)\n
                ![](./FCF_chart.png)
                """,
            context = context,
        )
