class Idioma:
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao


class Licao:
    def __init__(self, cod_licao, cod_idioma, total_niveis):
        self.cod_licao = cod_licao
        self.cod_idioma = cod_idioma
        self.total_niveis = total_niveis


class Exercicio:
    def __init__(
        self,
        cod_exercicio,
        cod_licao,
        nivel_dificuldade,
        descricao,
        opcoes_resposta,
        resposta_correta,
        pontuacao
    ):
        self.cod_exercicio = cod_exercicio
        self.cod_licao = cod_licao
        self.nivel_dificuldade = nivel_dificuldade
        self.descricao = descricao
        self.opcoes_resposta = opcoes_resposta
        self.resposta_correta = resposta_correta
        self.pontuacao = pontuacao


class Usuario:
    def __init__(
        self,
        codigo,
        nome,
        cod_idioma_aprendizado,
        nivel_atual,
        pontuacao_total
    ):
        self.codigo = codigo
        self.nome = nome
        self.cod_idioma_aprendizado = cod_idioma_aprendizado
        self.nivel_atual = nivel_atual
        self.pontuacao_total = pontuacao_total


class Acesso:
    def __init__(self, codigo_usuario, senha, tipo_acesso):
        self.codigo_usuario = codigo_usuario
        self.senha = senha
        self.tipo_acesso = tipo_acesso