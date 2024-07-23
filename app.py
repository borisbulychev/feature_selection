import json
import csv
import sys
from io import StringIO
from itertools import combinations
from mmh3 import hash as murmur3


def feature_selection(entities):
    """
    Функция для нахождения минимального набора признаков, однозначно идентифицирующих сущность.

    Параметры:
    entities (list): Список сущностей, каждая из которых представлена словарем с признаками.

    Возвращает:
    list: Список имен признаков, которые минимально идентифицируют сущности.
    """
    # Выделение имен признаков
    features = list(entities[0].keys())

    # Проверка всех комбинаций признаков
    for i in range(1, len(features) + 1):
        for feature_combination in combinations(features, i):
            hash_map = {}
            is_unique = True

            for entity in entities:
                # Создание ключа путем объединения значений признаков
                key = '_'.join(str(entity.get(feature, '')) for feature in feature_combination)

                hash_value = murmur3(key)

                if hash_value in hash_map:
                    is_unique = False
                    break
                hash_map[hash_value] = entity

            if is_unique:
                return list(feature_combination)

    return []


def main(json_file_path):
    """
    Функция для запуска кода. Принимает путь к JSON-файлу с данными и возвращает CSV-строку с минимальным набором имен признаков.

    Параметры:
    json_file_path (str): Путь к JSON-файлу, содержащему описание набора уникальных сущностей.

    Возвращает:
    str: CSV-строка с одной колонкой, содержащей искомый набор имен признаков.
    """
    try:
        # Чтение JSON-файла
        with open(json_file_path, 'r', encoding='utf-8') as file:
            entities = json.load(file)

        # Проверка на пустоту данных
        if not entities:
            return "Файл JSON пуст"

        # Нахождение минимального набора признаков
        key_features = feature_selection(entities)

        # Создание CSV-строки
        output = StringIO()
        writer = csv.writer(output)
        for feature in key_features:
            writer.writerow([feature])  # Значения признаков

        # Возвращение CSV-строки
        return output.getvalue()
    except FileNotFoundError:
        return "Файл не найден"
    except json.JSONDecodeError:
        return "Некорректные данные JSON"
    except Exception as e:
        return f"Произошла ошибка: {e}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python app.py <путь_к_json_файлу>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Вызов функции main и вывод результата
    result = main(json_file_path)
    print(result)
