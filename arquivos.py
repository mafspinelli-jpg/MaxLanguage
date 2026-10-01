import pickle


# IDIOMAS

def gravar_idioma(idioma):
    with open("dados/idiomas.dat", "ab") as arquivo:
        posicao = arquivo.tell()
        pickle.dump(idioma, arquivo)
    return posicao


def ler_idiomas():
    idiomas = []
    with open("dados/idiomas.dat", "rb") as arquivo:
        while True:
            try:
                idioma = pickle.load(arquivo)
                idiomas.append(idioma)
            except EOFError:
                break
    return idiomas


def ler_idioma_na_posicao(posicao):
    with open("dados/idiomas.dat", "rb") as arquivo:
        arquivo.seek(posicao)
        idioma = pickle.load(arquivo)
    return idioma


def carregar_indices_idiomas(arvore):
    with open("dados/idiomas.dat", "rb") as arquivo:
        while True:
            try:
                posicao = arquivo.tell()
                idioma = pickle.load(arquivo)
                arvore.inserir(idioma.codigo, posicao)
            except EOFError:
                break


# LIÇÕES

def gravar_licao(licao):
    with open("dados/licoes.dat", "ab") as arquivo:
        posicao = arquivo.tell()
        pickle.dump(licao, arquivo)
    return posicao


def ler_licoes():
    licoes = []
    with open("dados/licoes.dat", "rb") as arquivo:
        while True:
            try:
                licao = pickle.load(arquivo)
                licoes.append(licao)
            except EOFError:
                break
    return licoes


def ler_licao_na_posicao(posicao):
    with open("dados/licoes.dat", "rb") as arquivo:
        arquivo.seek(posicao)
        licao = pickle.load(arquivo)
    return licao


def carregar_indices_licoes(arvore):
    with open("dados/licoes.dat", "rb") as arquivo:
        while True:
            try:
                posicao = arquivo.tell()
                licao = pickle.load(arquivo)
                arvore.inserir(licao.cod_licao, posicao)
            except EOFError:
                break


# EXERCÍCIOS

def gravar_exercicio(exercicio):
    with open("dados/exercicios.dat", "ab") as arquivo:
        posicao = arquivo.tell()
        pickle.dump(exercicio, arquivo)
    return posicao


def ler_exercicios():
    exercicios = []
    with open("dados/exercicios.dat", "rb") as arquivo:
        while True:
            try:
                exercicio = pickle.load(arquivo)
                exercicios.append(exercicio)
            except EOFError:
                break
    return exercicios


def ler_exercicio_na_posicao(posicao):
    with open("dados/exercicios.dat", "rb") as arquivo:
        arquivo.seek(posicao)
        exercicio = pickle.load(arquivo)
    return exercicio


def carregar_indices_exercicios(arvore):
    with open("dados/exercicios.dat", "rb") as arquivo:
        while True:
            try:
                posicao = arquivo.tell()
                exercicio = pickle.load(arquivo)
                arvore.inserir(exercicio.cod_exercicio, posicao)
            except EOFError:
                break


def exercicios_permitidos(nivel_usuario):
    exercicios_permitidos = []
    exercicios = ler_exercicios()

    for exercicio in exercicios:
        if exercicio.nivel_dificuldade <= nivel_usuario:
            exercicios_permitidos.append(exercicio)

    return exercicios_permitidos


# USUÁRIOS

def gravar_usuario(usuario):
    with open("dados/usuarios.dat", "ab") as arquivo:
        posicao = arquivo.tell()
        pickle.dump(usuario, arquivo)
    return posicao


def ler_usuarios():
    usuarios = []
    with open("dados/usuarios.dat", "rb") as arquivo:
        while True:
            try:
                usuario = pickle.load(arquivo)
                usuarios.append(usuario)
            except EOFError:
                break
    return usuarios


def ler_usuario_na_posicao(posicao):
    with open("dados/usuarios.dat", "rb") as arquivo:
        arquivo.seek(posicao)
        usuario = pickle.load(arquivo)
    return usuario


def carregar_indices_usuarios(arvore):
    with open("dados/usuarios.dat", "rb") as arquivo:
        while True:
            try:
                posicao = arquivo.tell()
                usuario = pickle.load(arquivo)
                arvore.inserir(usuario.codigo, posicao)
            except EOFError:
                break


def atualizar_usuario(codigo_usuario, novo_usuario):
    usuarios = ler_usuarios()

    for i, usuario in enumerate(usuarios):
        if usuario.codigo == codigo_usuario:
            usuarios[i] = novo_usuario
            break

    with open("dados/usuarios.dat", "wb") as arquivo:
        for usuario in usuarios:
            pickle.dump(usuario, arquivo)


def excluir_usuario(codigo_usuario):
    usuarios = ler_usuarios()
    nova_lista = []
    encontrado = False

    for usuario in usuarios:
        if usuario.codigo == codigo_usuario:
            encontrado = True
        else:
            nova_lista.append(usuario)

    with open("dados/usuarios.dat", "wb") as arquivo:
        for usuario in nova_lista:
            pickle.dump(usuario, arquivo)

    return encontrado


# RANKING

def gerar_ranking():
    usuarios = ler_usuarios()
    ranking = sorted(
        usuarios,
        key=lambda usuario: usuario.pontuacao_total,
        reverse=True
    )
    return ranking


# ACESSOS

def gravar_acesso(acesso):
    with open("dados/acessos.dat", "ab") as arquivo:
        posicao = arquivo.tell()
        pickle.dump(acesso, arquivo)
    return posicao


def ler_acessos():
    acessos = []
    try:
        with open("dados/acessos.dat", "rb") as arquivo:
            while True:
                try:
                    acesso = pickle.load(arquivo)
                    acessos.append(acesso)
                except EOFError:
                    break
    except FileNotFoundError:
        pass
    return acessos


def carregar_indices_acessos(arvore):
    try:
        with open("dados/acessos.dat", "rb") as arquivo:
            while True:
                try:
                    posicao = arquivo.tell()
                    acesso = pickle.load(arquivo)
                    arvore.inserir(acesso.codigo_usuario, posicao)
                except EOFError:
                    break
    except FileNotFoundError:
        pass


def ler_acesso_na_posicao(posicao):
    with open("dados/acessos.dat", "rb") as arquivo:
        arquivo.seek(posicao)
        acesso = pickle.load(arquivo)
    return acesso


def excluir_acesso(codigo_usuario):
    acessos = ler_acessos()
    novos_acessos = []
    encontrado = False

    for acesso in acessos:
        if acesso.codigo_usuario == codigo_usuario:
            encontrado = True
        else:
            novos_acessos.append(acesso)

    if encontrado:
        with open("dados/acessos.dat", "wb") as arquivo:
            for acesso in novos_acessos:
                pickle.dump(acesso, arquivo)

    return encontrado