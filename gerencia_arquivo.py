import os
import hashlib
import re
import time
import getpass
import webbrowser

class INode:
    def __init__(self, filename, owner, size):
        # Representa um nó de índice (INode) que armazena informações sobre um arquivo
        self.filename = filename  # Nome do arquivo
        self.owner = owner  # Proprietário do arquivo
        self.size = size  # Tamanho do arquivo
        self.created_at = time.time()  # Tempo de criação do INode (atualizado no momento da criação)

class TreeNode:
    def __init__(self, name, is_directory=False):
        # Representa um nó em uma árvore de diretórios
        self.name = name
        self.is_directory = is_directory
        self.children = {}

class Bloco:
    def __init__(self, indice, tamanho):
        # Representa um bloco de dados no sistema de arquivos
        self.indice = indice  # Índice do bloco
        self.tamanho = tamanho  # Tamanho do bloco

class AlocacaoArquivos:
    def __init__(self, tamanho_total):
        # Gerencia a alocação e desalocação de arquivos no sistema de arquivos
        self.tamanho_total = tamanho_total  # Tamanho total do sistema de arquivos
        self.blocos_livres = [Bloco(0, tamanho_total)]  # Lista de blocos livres no sistema
        self.inodes = {}  # Dicionário para mapear caminhos de arquivo para seus respectivos INodes

    def alocar_arquivo(self, file_path, tamanho, owner):
        # Tenta alocar espaço para um arquivo no sistema
        blocos_a_alocar = self.encontrar_blocos_contiguos(tamanho)

        if blocos_a_alocar:
            # Remove os blocos alocados da lista de blocos livres
            self.blocos_livres = [bloco for bloco in self.blocos_livres if bloco not in blocos_a_alocar]

            # Cria um INode para o arquivo e o adiciona ao dicionário de INodes
            inode = INode(file_path, owner, tamanho)
            self.inodes[file_path] = inode

            return True
        else:
            print("Espaço contíguo insuficiente para alocar o arquivo.")
            return False

    def desalocar_arquivo(self, file_path):
        # Tenta desalocar espaço associado a um arquivo no sistema
        if file_path in self.inodes:
            # Recupera o tamanho do arquivo e cria blocos livres correspondentes
            tamanho = self.inodes[file_path].size
            blocos_desalocar = [Bloco(self.inodes[file_path].filename, tamanho)]
            self.blocos_livres.extend(blocos_desalocar)
            self.blocos_livres.sort(key=lambda x: x.indice)

            # Remove o INode associado ao arquivo
            del self.inodes[file_path]

    def encontrar_blocos_contiguos(self, tamanho):
        # Encontra blocos contíguos suficientes para alocar um arquivo do tamanho especificado
        blocos_contiguos = []
        tamanho_atual = 0

        for bloco in self.blocos_livres:
            tamanho_atual += bloco.tamanho
            blocos_contiguos.append(bloco)

            if tamanho_atual >= tamanho:
                break

        if tamanho_atual >= tamanho:
            return blocos_contiguos
        else:
            return []

class GerenciadorArquivos:
    def __init__(self):
        # Inicializa o gerenciador de arquivos com listas vazias para usuários e sem usuário autenticado
        self.usuarios = {}
        self.usuario_autenticado = None
        # Inicializa uma instância de AlocacaoArquivos com um tamanho total de 1000 unidades
        self.alocacao_arquivos = AlocacaoArquivos(tamanho_total=1000)

        # Adiciona a estrutura da árvore de diretórios ao gerenciador
        self.root_directory = TreeNode('root', is_directory=True)
        self.current_directory_node = self.root_directory

    def menu_principal(self):
        # Exibe o menu principal do gerenciador de arquivos
        print("\n--- Gerenciador de Arquivos ---")
        print("1. Acessar como Visitante")
        print("2. Criar Usuário")
        print("3. Fazer Login")
        print("4. Sair")

    def menu_logado(self):
        # Exibe o menu quando um usuário está autenticado
        print("\n--- Menu Logado ---")
        print("1. Operações com Arquivos")
        print("2. Operações com Diretórios")
        print("3. Sair")

    def menu_arquivos(self):
        # Exibe o menu de operações com arquivos
        print("\n--- Operações com Arquivos ---")
        print("1. Adicionar Arquivo (admin/user)")
        print("2. Remover Arquivo (admin)")
        print("3. Listar Arquivos (admin/user)")
        print("4. Abrir Arquivo (admin/user)")
        print("5. Ler Arquivo (admin/user/visitor)")
        print("6. Escrever em Arquivo (admin/user)")
        print("7. Renomear Arquivo (admin/user)")
        print("8. Adicionar ao Final do Arquivo (admin/user)")

    def menu_diretorios(self):
        # Exibe o menu de operações com diretórios
        print("\n--- Operações com Diretórios ---")
        print("1. Criar Diretório (admin/user)")
        print("2. Remover Diretório (admin)")
        print("3. Renomear Diretório (admin/user)")
        print("4. Abrir Diretório (admin/user)")

    def hash_password(self, password):
        # Gera uma hash da senha usando o algoritmo SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def check_credentials(self, username, password):
        # Verifica se as credenciais (nome de usuário e senha) estão corretas
        if username in self.usuarios and self.usuarios[username]['senha'] == self.hash_password(password):
            return self.usuarios[username]['funcao']  # Retorna a função (admin/user) do usuário
        return None  # Retorna None se as credenciais estiverem incorretas

    def acessar_como_visitante(self):
        # Permite acesso como visitante (somente leitura)
        print("Acesso como Visitante bem-sucedido.")
        self.usuario_autenticado = ("visitante", "visitor")

    def criar_usuario(self):
        # Cria um novo usuário com opção de admin ou user
        print("Opções de usuário: admin, user")
        role = input("Digite o tipo de usuário: ")

        if role not in ["admin", "user"]:
            print("Tipo de usuário inválido.")
            return

        username = input("Digite o nome de usuário: ")
        while username in self.usuarios:
            print("Nome de usuário já existe. Escolha outro.")
            username = input("Digite o nome de usuário: ")

        password = getpass.getpass("Digite a senha: ")

        self.usuarios[username] = {'senha': self.hash_password(password), 'funcao': role}
        print("Usuário criado com sucesso.")

    def fazer_login(self):
        # Realiza o processo de login
        username = input("Digite o nome de usuário: ")
        password = getpass.getpass("Digite a senha: ")

        role = self.check_credentials(username, password)

        if role:
            print(f"Login bem-sucedido. Função do usuário: {role}")
            self.usuario_autenticado = (username, role)  # Define o usuário autenticado
        else:
            print("Nome de usuário ou senha incorretos.")

    def operacoes_arquivos(self):
        # Executa operações de arquivos com base no tipo de usuário autenticado
        if self.usuario_autenticado[1] in ["admin", "user", "visitor"]:
            choice = input("Digite a opção desejada para arquivos: ")
            if self.usuario_autenticado[1] == "visitor":
                if choice == '5':
                    self.ler_arquivo()
                else:
                    print("Usuário só está autorizado a executar operação de leitura de arquivos.")
                    return
            if choice == '1':
                self.add_arquivos()
            elif choice == '2':
                self.remover_arquivos()
            elif choice == '3':
                self.listar_arquivos()
            elif choice == '4':
                self.abrir_arquivo()
            elif choice == '5':
                self.ler_arquivo()
            elif choice == '6':
                self.escrever_arquivo()
            elif choice == '7':
                self.renomear_arquivo()
            elif choice == '8':
                self.adicionar_final_arquivo()
            else:
                print("Opção inválida.")

    def operacoes_diretorios(self):
        # Executa operações de diretórios com base no tipo de usuário autenticado
        if self.usuario_autenticado[1] in ["admin", "user"]:
            choice = input("Digite a opção desejada para diretórios: ")
            if self.usuario_autenticado[1] == "user":
                if choice == '2':
                    print("Usuário não está autorizado a executar essa operação.")
                    return
            if choice == '1':
                self.criar_diretorio()
            elif choice == '2':
                self.remover_diretorio()
            elif choice == '3':
                self.renomear_diretorio()
            elif choice == '4':
                self.abrir_diretorio()
            else:
                print("Opção inválida.")
        else:
            print("Usuário não autorizado a executar operações com diretórios.")

    def sair(self):
        # Sai do programa
        print("Saindo do programa.")
        exit()

    def add_arquivos(self):
        # Adiciona um novo arquivo ao sistema
        file_name = input("Digite o nome do arquivo: ")
        if re.match("^[a-zA-Z0-9_.]+$", file_name):
            dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
            dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])

            # Certifique-se de que o diretório existe antes de criar o arquivo
            os.makedirs(dir_path, exist_ok=True)

            file_size = 1  # Tamanho do arquivo (pode ser ajustado)
            owner = self.usuario_autenticado[0]
            
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'w') as file:
                file.write('')
            print("Arquivo adicionado com sucesso.")
        else:
            print("Nome de arquivo inválido.")


    def remover_arquivos(self):
        # Remove um arquivo do sistema (somente para admin)
        if self.usuario_autenticado[1] == "admin":
            file_name = input("Digite o nome do arquivo: ")
            dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
            dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
            file_path = os.path.join(dir_path, file_name)
            if os.path.exists(file_path):
                self.alocacao_arquivos.desalocar_arquivo(file_name)
                os.remove(file_path)
                print("Arquivo removido com sucesso.")
            else:
                print("Arquivo não encontrado.")
        else:
            print("Usuário não autorizado a remover arquivos.")

    def listar_arquivos(self):
        # Lista arquivos em um diretório específico ou no diretório padrão
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_node = self.encontrar_diretorio(dir_name)

        if dir_node:
            print("\n--- Arquivos ---")
            for child_name, child_node in dir_node.children.items():
                print(child_name + (' [DIR]' if child_node.is_directory else ''))

    def abrir_arquivo(self):
        # Abre um arquivo no sistema (específico para sistemas Windows)
        file_name = input("Digite o nome do arquivo: ")
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
        file_path = os.path.join(dir_path, file_name)

        if os.path.exists(file_path):
            os.startfile(file_path)  # Isso é específico para sistemas Windows
        else:
            print("Arquivo não encontrado.")

    def ler_arquivo(self):
        # Lê o conteúdo de um arquivo
        file_name = input("Digite o nome do arquivo: ")
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
        file_path = os.path.join(dir_path, file_name)

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"Conteúdo do arquivo:\n{content}")
        except FileNotFoundError:
            print("Arquivo não encontrado.")

    def escrever_arquivo(self):
        # Escreve conteúdo em um arquivo
        file_name = input("Digite o nome do arquivo: ")
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
        file_path = os.path.join(dir_path, file_name)

        content = input("Digite o conteúdo a ser escrito no arquivo: ")

        # Certifica-se de que o diretório existe; se não, cria-o
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'w') as file:
            file.write(content)

        print("Conteúdo escrito no arquivo com sucesso.")

    def renomear_arquivo(self):
        # Renomeia um arquivo
        old_name = input("Digite o nome atual do arquivo: ")
        new_name = input("Digite o novo nome do arquivo: ")
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print("Arquivo renomeado com sucesso.")
        else:
            print("Arquivo não encontrado.")

    def adicionar_final_arquivo(self):
        # Adiciona conteúdo ao final de um arquivo
        file_name = input("Digite o nome do arquivo: ")
        dir_name = input("Digite o nome do diretório (deixe em branco para diretório padrão): ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name) if dir_name else os.path.join('directories', self.usuario_autenticado[0])
        file_path = os.path.join(dir_path, file_name)

        if os.path.exists(file_path):
            content = input("Digite o conteúdo a ser adicionado no final do arquivo: ")
            with open(file_path, 'a') as file:
                file.write(content)
            print("Conteúdo adicionado no final do arquivo com sucesso.")
        else:
            print("Arquivo não encontrado.")

    def encontrar_diretorio(self, path):
        # Encontra o nó de diretório correspondente a um caminho
        current_node = self.current_directory_node

        if path:
            components = path.split('/')
            for component in components:
                if component in current_node.children and current_node.children[component].is_directory:
                    current_node = current_node.children[component]
                else:
                    print(f"Diretório '{path}' não encontrado.")
                    return None

        return current_node

    def criar_subdiretorio(self, dir_path):
        # Cria um subdiretório
        # Use o separador de caminho ('/') para indicar a criação de um subdiretório dentro do diretório atual.
        os.makedirs(dir_path, exist_ok=True)
        print(f"Subdiretório '{dir_path}' criado com sucesso.")

    def criar_diretorio(self):
        # Cria um novo diretório ou subdiretório
        dir_name = input("Digite o nome do diretório: ")

        if os.path.sep in dir_name:
            # Se o nome do diretório contiver o separador de caminho, consideramos isso como
            # uma tentativa de criar um subdiretório dentro de um diretório existente.
            self.criar_subdiretorio(os.path.join('directories', self.usuario_autenticado[0], dir_name))
        else:
            dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name)

            # Certifique-se de que o diretório pai existe antes de criar o diretório
            os.makedirs(os.path.dirname(dir_path), exist_ok=True)

            os.makedirs(dir_path, exist_ok=True)  # Cria o diretório e não gera erro se já existir
            print(f"Diretório '{dir_name}' criado com sucesso.")


    def remover_diretorio(self):
        # Remove um diretório (somente para admin) e trata possíveis exceções
        if self.usuario_autenticado[1] == "admin":
            dir_name = input("Digite o nome do diretório: ")

            # Verifica se o diretório existe antes de removê-lo
            if dir_name in self.current_directory_node.children and self.current_directory_node.children[dir_name].is_directory:
                del self.current_directory_node.children[dir_name]
                print("Diretório removido com sucesso.")
            else:
                print("Diretório não encontrado.")
        else:
            print("Usuário não autorizado a remover diretórios.")

    def renomear_diretorio(self):
        # Renomeia um diretório
        old_name = input("Digite o nome atual do diretório: ")
        new_name = input("Digite o novo nome do diretório: ")

        old_path = os.path.join('directories', self.usuario_autenticado[0], old_name)
        new_path = os.path.join('directories', self.usuario_autenticado[0], new_name)

        # Certifique-se de que o diretório exista antes de tentar renomear
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print("Diretório renomeado com sucesso.")
        else:
            print("Diretório não encontrado. Verifique o nome informado.")

    def abrir_diretorio(self):
        # Abre um diretório no sistema
        dir_name = input("Digite o nome do diretório: ")
        dir_path = os.path.join('directories', self.usuario_autenticado[0], dir_name)

        # Certifique-se de que o diretório existe antes de tentar abrir
        if os.path.exists(dir_path):
            webbrowser.open(dir_path, new=2)  # Abre o diretório em um navegador de arquivos
            print(f"Diretório '{dir_name}' aberto com sucesso.")
        else:
            print(f"Diretório '{dir_name}' não encontrado.")

# ... Restante do código permanece o mesmo ...

# Instanciar o gerenciador
gerenciador = GerenciadorArquivos()

# Loop principal
while True:
    gerenciador.menu_principal()
    choice = input("Digite a opção desejada: ")

    if choice == '1':
        gerenciador.acessar_como_visitante()
    elif choice == '2':
        gerenciador.criar_usuario()
    elif choice == '3':
        gerenciador.fazer_login()
    elif choice == '4':
        gerenciador.sair()
    else:
        print("Opção inválida.")

    # Se o usuário estiver autenticado, mostrar menu correspondente
    while gerenciador.usuario_autenticado:
        gerenciador.menu_logado()
        choice = input("Digite a opção desejada: ")

        if choice == '1':
            gerenciador.menu_arquivos()
            gerenciador.operacoes_arquivos()
        elif choice == '2':
            gerenciador.menu_diretorios()
            gerenciador.operacoes_diretorios()
        elif choice == '3':
            gerenciador.usuario_autenticado = None
        else:
            print("Opção inválida.")
