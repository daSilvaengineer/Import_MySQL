# tests/test_database.py
import unittest
from unittest.mock import patch, MagicMock
from src.database import DatabaseManager
import mysql.connector

class TestDatabaseManager(unittest.TestCase):
    
    @patch('mysql.connector.connect')
    @patch('configparser.ConfigParser')
    def test_connect_success(self, mock_parser, mock_connect):
        """Testa conexão bem-sucedida"""
        # Configurar mocks
        mock_config = mock_parser.return_value
        mock_config.has_section.return_value = True
        mock_config.get.side_effect = lambda section, key: {
            'host': 'localhost',
            'user': 'test',
            'password': 'test123',
            'database': 'test_db',
            'port': '3306'
        }.get(key)
        
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        # Testar
        db_manager = DatabaseManager('config/db_config.ini')
        conn, cursor = db_manager.connect()
        
        # Verificar
        self.assertIsNotNone(conn)
        self.assertIsNotNone(cursor)
        mock_connect.assert_called_once()
    
    @patch('mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """Testa falha na conexão"""
        mock_connect.side_effect = mysql.connector.Error("Connection error")
        
        db_manager = DatabaseManager()
        conn, cursor = db_manager.connect()
        
        self.assertIsNone(conn)
        self.assertIsNone(cursor)
    
    @patch('mysql.connector.connect')
    def test_context_manager(self, mock_connect):
        """Testa o uso com context manager"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        with DatabaseManager() as (conn, cursor):
            self.assertIsNotNone(conn)
            self.assertIsNotNone(cursor)
        
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
