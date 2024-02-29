import os
import sys
import re
import datetime
import logging
from logging.handlers import RotatingFileHandler

def save_markdown(task_output):
    # Set the filename with today's date
    filename = "RESULT.md"
    # Write the task output to the markdown file
    with open(filename, 'w') as file:
        file.write(task_output.result)
    print(f"Newsletter saved as {filename}")



class LoggerWriter:
    def __init__(self, level):
        # 初始化 LoggerWriter 並設置其日誌級別
        self.level = level

    def write(self, message):
        # 如果消息不是空的，則寫入日誌
        if message != '\n':
            message = self.remove_ansi_codes(message)
            logging.log(self.level, message)

    def flush(self):
        # 此 flush 方法是為了滿足 file-like 對象的需求
        pass

    @staticmethod
    def remove_ansi_codes(message):
        return re.sub(r'\x1b\[.*?m', '', message)

def setup_logging():
    # 創建一個日誌器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 設置日誌格式
    log_format = logging.Formatter('%(message)s')

    # 創建一個流處理器，將日誌輸出到終端
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    # 創建一個文件處理器，用於將日誌寫入到文件 "CREWAI_IO.log"
    file_handler = RotatingFileHandler('CREWAI_IO.log', mode='w', encoding=None, delay=0)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # 在日誌文件中添加分割線和當前執行時間
    separator = '\n' + '=' * 39 + '\n'
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    execution_time_log = '|| 開始執行時間： ' + current_time + ' ||'
    padding_length = len(separator) - len(execution_time_log) - 2  # -2 for the newline characters in separator
    execution_time_log = execution_time_log.center(padding_length, ' ')
    logging.info(separator + execution_time_log + separator)

    # 將 sys.stdout 和 sys.stderr 重定向到日誌
    sys.stdout = LoggerWriter(logging.INFO)
    sys.stderr = LoggerWriter(logging.ERROR)

# 注意：此函數應在主腳本開始處調用，以配置日誌系統