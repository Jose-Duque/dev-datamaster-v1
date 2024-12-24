from astro.table import Table
from astro import sql as aql

class TransformToSilver:

    @aql.transform
    @staticmethod
    def estados(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_estados,
                SUBSTRING(estado, 1, 100) AS estado,
                SUBSTRING(sigla, 1, 2) AS sigla,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) AS data_inclusao_timestamp,
                CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT) AS data_atualizacao_timestamp
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def cidades(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_cidades,
                INITCAP(SUBSTRING(cidade, 1, 100)) AS nome_cidade, 
                id_estados,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao,
                COALESCE(CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT), CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT)) AS data_atualizacao 
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def clientes(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_clientes,
                INITCAP(cliente) AS cliente,
                TRIM(endereco) AS endereco,
                id_concessionarias,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao,
                COALESCE(CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT), CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT)) AS data_atualizacao
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def concessionarias(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_concessionarias,
                TRIM(concessionaria) AS nome_concessionaria, 
                id_cidades,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao,
                COALESCE(CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT), CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT)) AS data_atualizacao 
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def veiculos(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_veiculos,
                nome::VARCHAR(100),
                tipo,
                valor::DECIMAL(10,2) AS valor,
                CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT) AS data_atualizacao,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def vendas(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_vendas,
                id_veiculos,
                id_concessionarias,
                id_vendedores,
                id_clientes,
                valor_pago::DECIMAL(10,2) AS valor_venda, 
                CAST(TO_TIMESTAMP(data_venda / 1000.0) as TEXT) AS data_venda,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao,
                COALESCE(CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT), CAST(TO_TIMESTAMP(data_venda / 1000.0) as TEXT)) AS data_atualizacao
            FROM {{ table }}
        """
    
    @aql.transform
    @staticmethod
    def vendedores(table: Table):
        """
            Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
            Este exemplo seleciona algumas colunas e filtra os dados.
        """
        return """
            SELECT
                id_vendedores,
                INITCAP(nome::VARCHAR(100)) AS nome_vendedor, 
                id_concessionarias,
                CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT) as data_inclusao,
                COALESCE(CAST(TO_TIMESTAMP(data_atualizacao / 1000.0) as TEXT), CAST(TO_TIMESTAMP(data_inclusao / 1000.0) as TEXT)) AS data_atualizacao
            FROM {{ table }}
        """
    
    #TODO
    # @aql.transform
    # @staticmethod
    # def s_op_faturamento(s3_input_table_op_faturamento: Table):
    #     """
    #         Exemplo de transformação SQL. Você pode usar qualquer lógica SQL aqui.
    #         Este exemplo seleciona algumas colunas e filtra os dados.
    #     """
    #     return """
           
    #     """