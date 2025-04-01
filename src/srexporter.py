import pandas as pd
from database import DatabaseManager
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    """Classe para exportar dados do MySQL para Excel"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def export_to_excel(self, query: str, output_file: str = 'output.xlsx') -> bool:
        """
        Exporta dados de uma consulta SQL para um arquivo Excel
        
        Args:
            query: Consulta SQL para executar
            output_file: Nome do arquivo de saída
            
        Returns:
            bool: True se a exportação foi bem-sucedida
        """
        try:
            # Conectar ao banco de dados
            connection, cursor = self.db_manager.connect()
            
            if not cursor:
                return False
            
            # Executar consulta e obter dados
            cursor.execute(query)
            dados = cursor.fetchall()
            
            # Obter nomes das colunas
            colunas = [desc[0] for desc in cursor.description]
            
            # Criar DataFrame
            df = pd.DataFrame(dados, columns=colunas)
            
            # Exportar para Excel
            df.to_excel(output_file, index=False)
            logger.info(f"Dados exportados com sucesso para {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a exportação: {e}")
            return False
        finally:
            self.db_manager.disconnect()
