# Gerenciador de Arquivos em Python

Este é um programa simples em Python que simula um gerenciador de arquivos. Ele permite que os usuários realizem operações básicas de manipulação de arquivos e diretórios em um sistema simulado.

## Funcionalidades Principais

- **Autenticação de Usuários**
- **Operações com Arquivos**
- **Operações com Diretórios**

# Instrução para Criação de Subdiretórios:

- Ao criar um diretório, você pode usar o separador de caminho ('/') para indicar a criação de um subdiretório dentro do diretório atual.
  Por exemplo, se você quiser criar um subdiretório chamado "SO" dentro do diretório "Aulas", digite "Aulas/SO".
  Isso permitirá a criação de subdiretórios conforme necessário.

### Autenticação de Usuários

- **Acesso como Visitante:** Permite acesso somente para leitura.
- **Criação de Usuários:** Cria novos usuários como admin ou user.
- **Login:** Permite aos usuários existentes acessarem o sistema.
- **Logout:** Encerra a sessão do usuário.

### Operações com Arquivos

- **Adicionar Arquivo:** Adiciona um arquivo ao sistema (dependendo das permissões).
- **Remover Arquivo:** Remove um arquivo (apenas para admin).
- **Listar Arquivos:** Lista os arquivos em um diretório específico.
- **Abrir Arquivo:** Abre um arquivo no sistema (específico para Windows).
- **Ler Arquivo:** Exibe o conteúdo de um arquivo.
- **Escrever em Arquivo:** Permite escrever conteúdo em um arquivo existente.
- **Renomear Arquivo:** Altera o nome de um arquivo.
- **Adicionar ao Final do Arquivo:** Acrescenta conteúdo ao final de um arquivo.

### Operações com Diretórios

- **Criar Diretório:** Cria um novo diretório.
- **Remover Diretório:** Remove um diretório (apenas para admin).
- **Renomear Diretório:** Altera o nome de um diretório.
- **Abrir Diretório:** Abre um diretório no sistema (específico para Windows).
- **Fechar Diretório:** Encerra a operação no diretório.

### Requisitos

- Python 3.x instalado.
- Sistema operacional compatível (Windows).

### Execução

1. Faça o download ou clone este repositório.
2. Execute o arquivo `gerencia_arquivo.py`.

### Exemplo de Uso

- Ao iniciar o programa, será exibido um menu principal com opções para acessar como visitante, criar usuário, fazer login ou sair.
- Dependendo do tipo de usuário (visitante, user ou admin) e suas permissões, o menu oferece diferentes operações com arquivos e diretórios.
- Por exemplo, um visitante só pode realizar operações de leitura, enquanto um admin tem permissões para adicionar, remover e renomear arquivos/diretórios.
- As operações são realizadas através da interação com o menu e são aplicadas ao sistema simulado.

### Observações

- O programa simula um sistema de arquivos básico, utilizando estruturas de dados simplificadas.
- As operações são restritas de acordo com as permissões de usuário (visitante, user ou admin).
- O sistema de arquivos é puramente simulado em memória e não afeta o sistema de arquivos real do computador.


**Reconhecimentos e Direitos Autorais**

@Autores: João Gabriel de Oliveira Lopes, João Victor Lima Ewerton, Kauã Ferreira Galeno e Matheus Ryan Carreiro Costa Correia

@Contato: joao.gol@discente.ufma.br ; joao.ewerton@discente.ufma.br ; kaua.galeno@discente.ufma.br ; matheus.ryan@discente.ufma.br

@Data última versão: 10/12/23

@Versão: 1.0

@Outros repositórios: https://github.com/joaoisthedev ; https://github.com/Joao-Ewerton; https://github.com/k4uaxxxxx ; https://github.com/matheusryann

@Agradecimentos: Universidade Federal do Maranhão (UFMA), Professor Doutor Thales Levi Azevedo Valente, e colegas de curso.

@Copyright/License

Este material é resultado de um trabalho acadêmico para a disciplina SISTEMAS OPERACIONAIS, sobre a orientação do professor Dr. THALES LEVI AZEVEDO VALENTE, semestre letivo 2023.2, curso Engenharia da Computação, na Universidade Federal do Maranhão (UFMA). Todo o material sob esta licença é software livre: pode ser usado para fins acadêmicos e comerciais sem nenhum custo. Não há papelada, nem royalties, nem restrições de "copyleft" do tipo GNU. Ele é licenciado sob os termos da licença MIT reproduzida abaixo e, portanto, é compatível com GPL e também se qualifica como software de código aberto. É de domínio público. Os detalhes legais estão abaixo. O espírito desta licença é que você é livre para usar este material para qualquer finalidade, sem nenhum custo. O único requisito é que, se você usá-los, nos dê crédito.

Copyright © 2023 Educational Material

Este material está licenciado sob a Licença MIT. É permitido o uso, cópia, modificação, e distribuição deste material para qualquer fim, desde que acompanhado deste aviso de direitos autorais.

O MATERIAL É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM HIPÓTESE ALGUMA OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, OU EM CONEXÃO COM O MATERIAL OU O USO OU OUTRAS NEGOCIAÇÕES NO MATERIAL.

Para mais informações sobre a Licença MIT: https://opensource.org/licenses/MIT.