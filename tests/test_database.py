import unittest
from unittest.mock import patch, MagicMock
from database import create_connection, create_table, insert_url

class TestDatabase(unittest.TestCase):

    @patch('database.psycopg2.connect')
    def test_create_connection(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        conn = create_connection()
        self.assertEqual(conn, mock_connection)
        mock_connect.assert_called_once_with(
            dbname="my_dog_project",
            user="daniela",
            password="daniela123",
            host="localhost",
            port="5432"
        )

    @patch('database.create_connection')
    def test_create_table(self, mock_create_connection):
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        create_table()
        mock_conn.cursor().execute.assert_called_once_with("""
            CREATE TABLE IF NOT EXISTS dog_images (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL
            )
        """)
        mock_conn.commit.assert_called_once()
        mock_conn.cursor().close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('database.create_connection')
    def test_insert_url(self, mock_create_connection):
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        insert_url('http://example.com/image.jpg')
        mock_conn.cursor().execute.assert_called_once_with(
            "INSERT INTO dog_images (url) VALUES (%s)",
            ('http://example.com/image.jpg',)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.cursor().close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
