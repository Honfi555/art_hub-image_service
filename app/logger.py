"""Файл для настройки логирования."""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

__all__: list[str] = ["configure_logs"]


def create_intermediate_dirs(path: str) -> None:
	"""
	Создаёт всё директории в указанном пути.
	:param path: Путь для создания папок, может оканчиваться на файл.
	"""
	try:
		if not path.endswith(os.sep):
			dir_path = os.path.dirname(path)
		else:
			dir_path = path
		os.makedirs(dir_path, exist_ok=True)
	except Exception as e:
		print("Ошибка при создании директорий: %s", e)


def configure_logs(name: str, logs_path: str = "logs/app.log", log_level: int = logging.INFO) -> logging.Logger:
	"""
	Настраивает вывод и сохранение логов в файл и вывод в консоль.
	:param name: Название файла, в котором создаётся логгер.
	:param log_level: Урень логирования, стандартное значение INFO.
	:param logs_path: Путь к файлу с логами.
	"""

	# Получаем корневой логгер
	logger = logging.getLogger(name=name)
	logger.setLevel(log_level)

	# Проверяем, есть ли уже обработчики, чтобы избежать добавления дубликатов
	if not logger.handlers:
		create_intermediate_dirs(path=logs_path)
		# Настройка RotatingFileHandler для файла логов с максимальным размером 50 МБ и 3 резервными копиями
		file_handler = RotatingFileHandler(
			logs_path,
			mode='a',
			maxBytes=50 * 1024 * 1024,  # 50 МБ
			backupCount=3,
			encoding='utf-8'
		)
		file_handler.setLevel(log_level)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

		# Добавляем обработчик для консоли
		console_handler = logging.StreamHandler(sys.stdout)
		console_handler.setLevel(log_level)
		console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

		logger.addHandler(file_handler)
		logger.addHandler(console_handler)

	return logger


if __name__ == "__main__":
	configure_logs(__name__)
	logging.info("Это информационное сообщение")
	logging.warning("Это предупреждающее сообщение")
	logging.error("Это сообщение об ошибке")
	print("Это сообщение через print()")
