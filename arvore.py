class No:
    def __init__(self, chave, posicao):
        self.chave = chave
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def buscar(self, chave):
        atual = self.raiz

        while atual is not None:
            if chave == atual.chave:
                return atual.posicao

            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None

    def inserir(self, chave, posicao):
        novo_no = No(chave, posicao)

        if self.raiz is None:
            self.raiz = novo_no
            return True

        atual = self.raiz

        while True:
            if chave < atual.chave:
                if atual.esquerda is None:
                    atual.esquerda = novo_no
                    return True
                atual = atual.esquerda

            elif chave > atual.chave:
                if atual.direita is None:
                    atual.direita = novo_no
                    return True
                atual = atual.direita

            else:
                return False

    def em_ordem(self, no):
        if no is not None:
            self.em_ordem(no.esquerda)
            print(no.chave)
            self.em_ordem(no.direita)