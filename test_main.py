import unittest
from unittest.mock import patch, Mock
from main import Cashier, conn, c  # Імпортуйте ваші класи та об'єкти


class TestCashier(unittest.TestCase):

    @patch('main.c')  # Замінили на 'main.c'
    @patch('main.conn')
    def test_save_update(self, mock_conn, mock_c):
        # Створення касира з заданим ID (оновлення запису)
        cashier = Cashier(cashier_id=1, name='John Doe', phone_number='1234567890', email='john@example.com')
        cashier.save()

        # Перевірка, що викликається правильний SQL-запит для оновлення
        mock_c.execute.assert_called_with(
            """UPDATE Cashier SET name=?, phone_number=?, email=? WHERE cashier_id=?""",
            ('John Doe', '1234567890', 'john@example.com', 1)
        )
        mock_conn.commit.assert_called_once()

    @patch('main.c')
    @patch('main.conn')
    def test_save_insert(self, mock_conn, mock_c):
        # Створення нового касира (без ID)
        cashier = Cashier(name='Jane Doe', phone_number='0987654321', email='jane@example.com')
        cashier.save()

        # Перевірка, що викликається правильний SQL-запит для вставки
        mock_c.execute.assert_called_with(
            """INSERT INTO Cashier (name, phone_number, email) VALUES (?, ?, ?)""",
            ('Jane Doe', '0987654321', 'jane@example.com')
        )
        mock_conn.commit.assert_called_once()

    @patch('main.c')
    @patch('main.conn')
    def test_delete(self, mock_conn, mock_c):
        # Видалення касира
        cashier = Cashier(cashier_id=1)
        cashier.delete()

        # Перевірка, що викликається правильний SQL-запит для видалення
        mock_c.execute.assert_called_with(
            """DELETE FROM Cashier WHERE cashier_id=?""",
            (1,)
        )
        mock_conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
