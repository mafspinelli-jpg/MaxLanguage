from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from arvore import ArvoreBinaria
from modelos import (
    Usuario,
    Acesso,
    Idioma,
    Licao,
    Exercicio
)
from arquivos import (
    carregar_indices_usuarios,
    carregar_indices_acessos,
    carregar_indices_idiomas,
    carregar_indices_licoes,
    carregar_indices_exercicios,
    ler_usuario_na_posicao,
    ler_acesso_na_posicao,
    ler_licao_na_posicao,
    ler_usuarios,
    ler_idiomas,
    ler_licoes,
    ler_exercicios,
    gravar_usuario,
    gravar_acesso,
    gravar_idioma,
    gravar_licao,
    gravar_exercicio,
    atualizar_usuario,
    excluir_usuario,
    excluir_acesso,
    gerar_ranking
)

app = Flask(__name__)
app.secret_key = "maxlanguage-chave"

arvore_usuarios = ArvoreBinaria()
arvore_acessos = ArvoreBinaria()
arvore_idiomas = ArvoreBinaria()
arvore_licoes = ArvoreBinaria()
arvore_exercicios = ArvoreBinaria()


def carregar_todos_indices():
    indices = [
        (arvore_usuarios, carregar_indices_usuarios),
        (arvore_acessos, carregar_indices_acessos),
        (arvore_idiomas, carregar_indices_idiomas),
        (arvore_licoes, carregar_indices_licoes),
        (arvore_exercicios, carregar_indices_exercicios),
    ]

    for arvore, carregar in indices:
        arvore.raiz = None
        try:
            carregar(arvore)
        except FileNotFoundError:
            pass


def recarregar_indice(arvore, funcao_carregar):
    arvore.raiz = None
    try:
        funcao_carregar(arvore)
    except FileNotFoundError:
        pass


carregar_todos_indices()


def verificar_admin():
    return session.get("tipo_acesso") == "admin"


def verificar_usuario():
    return session.get("tipo_acesso") == "usuario"


@app.route("/", methods=["GET", "POST"])
def login():
    mensagem = ""

    if request.method == "POST":
        codigo_texto = request.form.get("codigo")
        senha = request.form.get("senha")

        try:
            codigo = int(codigo_texto)
        except (ValueError, TypeError):
            return render_template("login.html", mensagem="Código ou senha inválidos.")

        posicao = arvore_acessos.buscar(codigo)

        if posicao is None:
            return render_template("login.html", mensagem="Código ou senha inválidos.")

        acesso = ler_acesso_na_posicao(posicao)

        if acesso.senha != senha:
            return render_template("login.html", mensagem="Código ou senha inválidos.")

        if acesso.tipo_acesso == "admin":
            session["codigo"] = codigo
            session["tipo_acesso"] = "admin"
            return redirect(url_for("admin"))

        posicao_usuario = arvore_usuarios.buscar(codigo)

        if posicao_usuario is None:
            return render_template("login.html", mensagem="Usuário não encontrado.")

        usuario = ler_usuario_na_posicao(posicao_usuario)

        session["codigo"] = usuario.codigo
        session["tipo_acesso"] = "usuario"

        return redirect(url_for("usuario"))

    return render_template("login.html", mensagem=mensagem)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro():
    idiomas = ler_idiomas()

    if request.method == "POST":
        try:
            codigo = int(request.form.get("codigo"))
            cod_idioma = int(request.form.get("cod_idioma"))
        except (ValueError, TypeError):
            return render_template(
                "cadastro.html",
                idiomas=idiomas,
                mensagem="Código e idioma precisam ser números válidos."
            )

        nome = (request.form.get("nome") or "").strip()
        senha = (request.form.get("senha") or "").strip()

        if (
            arvore_usuarios.buscar(codigo) is not None
            or arvore_acessos.buscar(codigo) is not None
        ):
            return render_template(
                "cadastro.html",
                idiomas=idiomas,
                mensagem="Esse código já está em uso. Escolha outro."
            )

        if arvore_idiomas.buscar(cod_idioma) is None:
            return render_template(
                "cadastro.html",
                idiomas=idiomas,
                mensagem="Escolha um idioma válido."
            )

        if nome == "" or senha == "":
            return render_template(
                "cadastro.html",
                idiomas=idiomas,
                mensagem="Preencha nome e senha."
            )

        gravar_usuario(Usuario(codigo, nome, cod_idioma, 1, 0))
        gravar_acesso(Acesso(codigo, senha, "usuario"))

        recarregar_indice(arvore_usuarios, carregar_indices_usuarios)
        recarregar_indice(arvore_acessos, carregar_indices_acessos)

        return redirect(url_for("login", sucesso="cadastrado"))

    return render_template("cadastro.html", idiomas=idiomas, mensagem="")


@app.route("/admin")
def admin():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template("admin/admin.html")


@app.route("/admin/usuarios")
def usuarios():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template(
        "admin/usuarios.html",
        usuarios=ler_usuarios(),
        idiomas=ler_idiomas()
    )


@app.route("/admin/usuarios/cadastrar", methods=["POST"])
def cadastrar_usuario_web():
    if not verificar_admin():
        return redirect(url_for("login"))

    try:
        codigo = int(request.form.get("codigo"))
        cod_idioma = int(request.form.get("cod_idioma"))
    except (ValueError, TypeError):
        return redirect(url_for("usuarios", erro="dados_invalidos"))

    nome = (request.form.get("nome") or "").strip()
    senha = (request.form.get("senha") or "").strip()

    if arvore_usuarios.buscar(codigo) is not None:
        return redirect(url_for("usuarios", erro="usuario_existente"))

    if arvore_idiomas.buscar(cod_idioma) is None:
        return redirect(url_for("usuarios", erro="idioma_invalido"))

    if nome == "" or senha == "":
        return redirect(url_for("usuarios", erro="campos_obrigatorios"))

    gravar_usuario(Usuario(codigo, nome, cod_idioma, 1, 0))
    gravar_acesso(Acesso(codigo, senha, "usuario"))

    recarregar_indice(arvore_usuarios, carregar_indices_usuarios)
    recarregar_indice(arvore_acessos, carregar_indices_acessos)

    return redirect(url_for("usuarios", sucesso="cadastrado"))


@app.route("/admin/usuarios/excluir/<int:codigo>", methods=["POST"])
def excluir_usuario_web(codigo):
    if not verificar_admin():
        return redirect(url_for("login"))

    if arvore_usuarios.buscar(codigo) is None:
        return redirect(url_for("usuarios", erro="usuario_nao_encontrado"))

    if not excluir_usuario(codigo):
        return redirect(url_for("usuarios", erro="usuario_nao_encontrado"))

    excluir_acesso(codigo)

    recarregar_indice(arvore_usuarios, carregar_indices_usuarios)
    recarregar_indice(arvore_acessos, carregar_indices_acessos)

    return redirect(url_for("usuarios", sucesso="excluido"))


@app.route("/admin/idiomas")
def idiomas():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template("admin/idiomas.html", idiomas=ler_idiomas())


@app.route("/admin/idiomas/cadastrar", methods=["POST"])
def cadastrar_idioma_web():
    if not verificar_admin():
        return redirect(url_for("login"))

    try:
        codigo = int(request.form.get("codigo"))
    except (ValueError, TypeError):
        return redirect(url_for("idiomas", erro="dados_invalidos"))

    descricao = (request.form.get("descricao") or "").strip()

    if arvore_idiomas.buscar(codigo) is not None:
        return redirect(url_for("idiomas", erro="idioma_existente"))

    if descricao == "":
        return redirect(url_for("idiomas", erro="descricao_vazia"))

    gravar_idioma(Idioma(codigo, descricao))

    recarregar_indice(arvore_idiomas, carregar_indices_idiomas)

    return redirect(url_for("idiomas", sucesso="cadastrado"))


@app.route("/admin/licoes")
def licoes():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template(
        "admin/licoes.html",
        licoes=ler_licoes(),
        idiomas=ler_idiomas()
    )


@app.route("/admin/licoes/cadastrar", methods=["POST"])
def cadastrar_licao_web():
    if not verificar_admin():
        return redirect(url_for("login"))

    try:
        cod_licao = int(request.form.get("cod_licao"))
        cod_idioma = int(request.form.get("cod_idioma"))
        total_niveis = int(request.form.get("total_niveis"))
    except (ValueError, TypeError):
        return redirect(url_for("licoes", erro="dados_invalidos"))

    if arvore_licoes.buscar(cod_licao) is not None:
        return redirect(url_for("licoes", erro="licao_existente"))

    if arvore_idiomas.buscar(cod_idioma) is None:
        return redirect(url_for("licoes", erro="idioma_invalido"))

    if total_niveis <= 0:
        return redirect(url_for("licoes", erro="total_niveis_invalido"))

    gravar_licao(Licao(cod_licao, cod_idioma, total_niveis))

    recarregar_indice(arvore_licoes, carregar_indices_licoes)

    return redirect(url_for("licoes", sucesso="cadastrado"))


@app.route("/admin/exercicios")
def exercicios():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template(
        "admin/exercicios.html",
        exercicios=ler_exercicios(),
        licoes=ler_licoes(),
        idiomas=ler_idiomas()
    )


@app.route("/admin/exercicios/cadastrar", methods=["POST"])
def cadastrar_exercicio_web():
    if not verificar_admin():
        return redirect(url_for("login"))

    try:
        codigo = int(request.form.get("codigo"))
        cod_licao = int(request.form.get("cod_licao"))
        nivel = int(request.form.get("nivel"))
        pontuacao = float(request.form.get("pontuacao"))
    except (ValueError, TypeError):
        return redirect(url_for("exercicios", erro="dados_invalidos"))

    descricao = request.form.get("descricao")
    resposta_correta = request.form.get("resposta_correta")

    opcoes_resposta = [
        request.form.get("opcao_a"),
        request.form.get("opcao_b"),
        request.form.get("opcao_c"),
        request.form.get("opcao_d"),
    ]

    if arvore_exercicios.buscar(codigo) is not None:
        return redirect(url_for("exercicios", erro="exercicio_existente"))

    posicao_licao = arvore_licoes.buscar(cod_licao)

    if posicao_licao is None:
        return redirect(url_for("exercicios", erro="licao_invalida"))

    licao = ler_licao_na_posicao(posicao_licao)

    if nivel < 1 or nivel > licao.total_niveis:
        return redirect(url_for("exercicios", erro="nivel_invalido"))

    if not descricao or descricao.strip() == "":
        return redirect(url_for("exercicios", erro="descricao_vazia"))

    gravar_exercicio(
        Exercicio(
            codigo,
            cod_licao,
            nivel,
            descricao.strip(),
            opcoes_resposta,
            resposta_correta,
            pontuacao
        )
    )

    recarregar_indice(arvore_exercicios, carregar_indices_exercicios)

    return redirect(url_for("exercicios", sucesso="cadastrado"))


@app.route("/admin/ranking")
def ranking():
    if not verificar_admin():
        return redirect(url_for("login"))

    return render_template("admin/ranking.html", ranking=gerar_ranking())


@app.route("/usuario")
def usuario():
    if not verificar_usuario():
        return redirect(url_for("login"))

    posicao = arvore_usuarios.buscar(session.get("codigo"))

    if posicao is None:
        session.clear()
        return redirect(url_for("login"))

    usuario = ler_usuario_na_posicao(posicao)

    nome_idioma = "Idioma não encontrado"

    for idioma in ler_idiomas():
        if idioma.codigo == usuario.cod_idioma_aprendizado:
            nome_idioma = idioma.descricao
            break

    return render_template(
        "usuario/usuario.html",
        usuario=usuario,
        idioma=nome_idioma,
        concluiu=usuario_concluiu_idioma(usuario)
    )


def _exercicios_do_nivel(usuario):
    disponiveis = []

    for exercicio in ler_exercicios():
        posicao_licao = arvore_licoes.buscar(exercicio.cod_licao)

        if posicao_licao is None:
            continue

        licao = ler_licao_na_posicao(posicao_licao)

        if (
            licao.cod_idioma == usuario.cod_idioma_aprendizado
            and exercicio.nivel_dificuldade <= usuario.nivel_atual
        ):
            disponiveis.append(exercicio)

    return disponiveis


def _total_niveis_do_idioma(usuario):
    for licao in ler_licoes():
        if licao.cod_idioma == usuario.cod_idioma_aprendizado:
            return licao.total_niveis

    return 1


def usuario_concluiu_idioma(usuario):
    total_niveis = _total_niveis_do_idioma(usuario)
    return usuario.nivel_atual >= total_niveis


@app.route("/usuario/exercicios", methods=["GET", "POST"])
def praticar():
    if not verificar_usuario():
        return redirect(url_for("login"))

    posicao_usuario = arvore_usuarios.buscar(session.get("codigo"))

    if posicao_usuario is None:
        session.clear()
        return redirect(url_for("login"))

    usuario = ler_usuario_na_posicao(posicao_usuario)
    exercicios_disponiveis = _exercicios_do_nivel(usuario)

    try:
        indice = int(request.args.get("indice", 0))
    except (ValueError, TypeError):
        indice = 0

    if request.method == "POST":
        codigo_exercicio = int(request.form.get("codigo_exercicio"))
        resposta = request.form.get("resposta")

        exercicio = next(
            (e for e in exercicios_disponiveis if e.cod_exercicio == codigo_exercicio),
            None
        )

        if exercicio is None:
            return redirect(url_for("praticar"))

        if resposta == exercicio.resposta_correta:
            usuario.pontuacao_total += exercicio.pontuacao
            mensagem = f"Resposta correta! +{exercicio.pontuacao} pontos."
        else:
            desconto = exercicio.pontuacao * 0.10
            usuario.pontuacao_total = max(0, usuario.pontuacao_total - desconto)
            mensagem = f"Resposta incorreta. -{desconto} pontos."

        total_niveis = _total_niveis_do_idioma(usuario)

        if usuario.pontuacao_total >= usuario.nivel_atual * 100:
            if usuario.nivel_atual < total_niveis:
                usuario.nivel_atual += 1
                mensagem += f" Você avançou para o nível {usuario.nivel_atual}!"

        atualizar_usuario(usuario.codigo, usuario)
        recarregar_indice(arvore_usuarios, carregar_indices_usuarios)

        return redirect(url_for("praticar", indice=indice + 1, mensagem=mensagem))

    mensagem = request.args.get("mensagem", "")
    total = len(exercicios_disponiveis)
    exercicio_atual = exercicios_disponiveis[indice] if indice < total else None

    return render_template(
        "usuario/exercicios.html",
        usuario=usuario,
        exercicio=exercicio_atual,
        indice=indice,
        total=total,
        mensagem=mensagem
    )


@app.route("/usuario/certificado")
def certificado():
    if not verificar_usuario():
        return redirect(url_for("login"))

    posicao = arvore_usuarios.buscar(session.get("codigo"))

    if posicao is None:
        session.clear()
        return redirect(url_for("login"))

    usuario = ler_usuario_na_posicao(posicao)

    if not usuario_concluiu_idioma(usuario):
        return redirect(url_for("usuario"))

    nome_idioma = "Idioma não encontrado"

    for idioma in ler_idiomas():
        if idioma.codigo == usuario.cod_idioma_aprendizado:
            nome_idioma = idioma.descricao
            break

    return render_template(
        "usuario/certificado.html",
        usuario=usuario,
        idioma=nome_idioma,
        data_emissao=date.today().strftime("%d/%m/%Y")
    )


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)