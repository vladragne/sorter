import os
import shutil
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. Указываем папку, в которой нужно навести порядок.
# По умолчанию скрипт будет прибираться в папке "Test_Folder" рядом с вашим кодом.
TARGET_DIR = "./Test_Folder"

# 2. Карта сортировки: расширение файла -> имя итоговой папки
FILE_TYPES = {
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Документы": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx"],
    "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Музыка и Аудио": [".mp3", ".wav", ".flac", ".m4a"],
    "Видео": [".mp4", ".avi", ".mkv", ".mov"],
    "Программы и Скрипты": [".exe", ".msi", ".py", ".bat"]
}

def create_folders_if_not_exists(base_path, folder_names):
    """Создает папки для категорий, если их еще нет"""
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Создана папка для категории: {folder}")

def get_category(file_extension):
    """Определяет категорию по расширению файла"""
    ext = file_extension.lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Другое"  # Если расширение неизвестно

def sort_files():
    # Проверяем, существует ли целевая папка
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        logging.warning(f"Папка {TARGET_DIR} не существовала и была создана. Наполните её файлами для теста!")
        return

    logging.info(f"Запуск сортировки в папке: {os.path.abspath(TARGET_DIR)}")

    # Создаем необходимые папки (Изображения, Документы и т.д.) внутри целевой папки
    create_folders_if_not_exists(TARGET_DIR, list(FILE_TYPES.keys()) + ["Другое"])

    # Получаем список всех элементов в папке
    all_items = os.listdir(TARGET_DIR)
    
    moved_count = 0

    for item in all_items:
        item_path = os.path.join(TARGET_DIR, item)

        # Пропускаем папки, сортируем ТОЛЬКО файлы
        if os.path.isdir(item_path):
            continue

        # Получаем имя файла и его расширение
        file_name, file_ext = os.path.splitext(item)

        # Пропускаем сам файл скрипта, если он вдруг лежит в этой же папке
        if item == "sorter.py":
            continue

        # Определяем, в какую папку отправить файл
        category = get_category(file_ext)
        destination_dir = os.path.join(TARGET_DIR, category)
        destination_path = os.path.join(destination_dir, item)

        # Безопасно перемещаем файл
        try:
            shutil.move(item_path, destination_path)
            logging.info(f"Файл '{item}' перемещен в паку '{category}'")
            moved_count += 1
        except Exception as e:
            logging.error(f"Не удалось переместить файл {item}: {e}")

    logging.info(f"🎉 Сортировка успешно завершена! Наведено в порядок файлов: {moved_count}")

if __name__ == "__main__":
    sort_files()
