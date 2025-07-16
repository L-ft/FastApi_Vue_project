import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    # 创建日志目录
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # 文件日志处理器（带轮转）
    file_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10240000, backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 获取根日志记录器并添加处理器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 将日志器附加到应用
    app.state.logger = logger

    return logger