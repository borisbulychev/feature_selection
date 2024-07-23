import unittest
import json
from io import StringIO
import csv
from app import feature_selection, main


class TestFeatureSelection(unittest.TestCase):

    def setUp(self):
        self.json_data_1 = json.dumps([
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "6"},
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "7"},
            {"фамилия": "Петров", "имя": "Иван", "отчество": "Сергеевич", "класс": "7"}
        ])
        self.entities_1 = json.loads(self.json_data_1)

    def test_feature_selection(self):
        result = feature_selection(self.entities_1)

        # Ожидаемый результат, если он верен согласно вашему заданию
        expected_result = ["фамилия", "класс"]

        # Проверка результата
        self.assertEqual(result, expected_result)


class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.json_data_1 = json.dumps([
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "6"},
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "7"},
            {"фамилия": "Петров", "имя": "Иван", "отчество": "Сергеевич", "класс": "7"}
        ])
        self.json_file_path = 'test_data.json'

        # Создание тестового JSON-файла
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            file.write(self.json_data_1)

    def test_main(self):
        result_csv = main(self.json_file_path)
        self.assertIsInstance(result_csv, str)

        # Используем StringIO для обработки CSV строки
        result_io = StringIO(result_csv)
        reader = csv.reader(result_io)
        rows = list(reader)

        # Проверка количества строк в CSV
        self.assertGreater(len(rows), 0, "CSV должно содержать хотя бы одну строку.")

        # Проверка количества строк
        expected_num_rows = len(feature_selection(json.loads(self.json_data_1)))
        self.assertEqual(len(rows), expected_num_rows, "Количество строк в CSV должно соответствовать количеству признаков.")


if __name__ == "__main__":
    unittest.main()
