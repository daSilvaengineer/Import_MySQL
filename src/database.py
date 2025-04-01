import mysql.connector
from configparser import ConfigParser
import logging
from typing import Optional, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Classe para gerenciar conexões com o banco de dados MySQL"""
    
    def __init__(self, config_file: str = 'config/db_config.ini'):
        self.config_file = config_file
        self.connection = None
        self.cursor = None
    
    def _load_config(self) -> dict:
        """Carrega configurações do arquivo .ini"""
        parser = ConfigParser()
        parser.read(self.config_file)
        
        if not parser.has_section('mysql'):
            raise ValueError(f'Seção [mysql] não encontrada no arquivo {self.config_file}')
            
        return {
            'host': parser.get('mysql', 'host'),
            'user': parser.get('mysql', 'user'),
            'password': parser.get('mysql', 'password'),
            'database': parser.get('mysql', 'database'),
            'port': parser.getint('mysql', 'port', fallback=3306)
        }
    
    def connect(self) -> Tuple[Optional[mysql.connector.MySQLConnection], Optional[mysql.connector.cursor.MySQLCursor]]:
        """Estabelece conexão com o banco de dados"""
        try:
            db_config = self._load_config()
            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Conexão bem-sucedida com o banco de dados!")
            return self.connection, self.cursor
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            return None, None
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexão fechada.")
    
    def __enter__(self):
        """Suporte para gerenciador de contexto"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garante que a conexão será fechada"""
        self.disconnect()
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Executa uma consulta SQL e retorna os resultados"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao executar consulta: {e}")
            raise
