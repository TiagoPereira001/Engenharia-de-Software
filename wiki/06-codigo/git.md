# Git e pull requests

[Índice](../README.md) · [← Testes](testes.md) · [Equipa e papéis →](../07-scrum/equipa-e-papeis.md)

- Há uma branch principal, a `main`.
- Cada cartão do Jira tem a sua branch: `feature/EDS-164-ambiente`.
- Cada pessoa faz commit do seu próprio trabalho, com a sua conta. É o histórico do Git que mostra quem fez o quê.
- Mensagens de commit no formato da secção [Mensagens de commit](#mensagens-de-commit), mais abaixo.
- O trabalho volta à `main` por pull request. Outra pessoa revê e aprova.
- O GitHub Actions tem de estar verde.
- Se a IA ajudou, diz-se no pull request para quê, e acrescenta-se uma linha ao registo de uso de IA (`docs/registo-ia/registo_uso_ia.tex`).
- Palavras-passe e chaves nunca entram no repositório.

A definição de concluído completa está no epic [EDS-158](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-158).

```bash
git switch main
git pull
git switch -c feature/EDS-167-submeter-pedido
```

## Mensagens de commit

Seguimos os [padrões de commits](https://github.com/iuricode/padroes-de-commits), que se baseiam nos [Conventional Commits](https://www.conventionalcommits.org/pt-br). Desde 28/10/2026 todos os commits usam este formato:

```text
:emoji: tipo(âmbito): descrição
```

- **emoji:** o código do emoji do tipo, da tabela abaixo. O GitHub mostra-o como imagem.
- **tipo:** diz a intenção do commit (`feat`, `fix`, `docs`...).
- **(âmbito):** opcional, a parte do projeto que mudou, em minúsculas: `pedidos`, `contas`, `frontend`, `docker`, `wiki`, `readme`, `modelacao`, `registo-ia`.
- **descrição:** curta (até umas quatro ou cinco palavras), em português de Portugal, a dizer o que fizemos.
- **Rodapé:** opcional, a chave do cartão do Jira numa linha à parte, depois de uma linha em branco: `Refs: EDS-169`.

Um `!` depois do tipo ou do âmbito marca uma mudança que parte o que já existia: `feat(api)!: ...`.

| Emoji | Código | Tipo | Quando |
|---|---|---|---|
| ✨ | `:sparkles:` | `feat` | Funcionalidade nova |
| 💄 | `:lipstick:` | `feat` | Aspeto da interface (CSS, ecrãs) |
| 🐛 | `:bug:` | `fix` | Correção de um erro |
| 📚 | `:books:` | `docs` | Documentação: README, wiki, LaTeX, diagramas |
| 💡 | `:bulb:` | `docs` | Comentários no código |
| 🧪 | `:test_tube:` | `test` | Testes novos ou alterados |
| ➕ | `:heavy_plus_sign:` | `build` | Dependência nova |
| ➖ | `:heavy_minus_sign:` | `build` | Dependência removida |
| 🧱 | `:bricks:` | `ci` | Docker e GitHub Actions |
| 🔧 | `:wrench:` | `chore` | Configuração |
| 🙈 | `:see_no_evil:` | `chore` | `.gitignore` |
| 🚚 | `:truck:` | `chore` | Mover ou mudar o nome de ficheiros |
| ♻️ | `:recycle:` | `refactor` | Reorganizar código sem mudar o que faz |
| ⚡ | `:zap:` | `perf` | Desempenho |
| 🗃️ | `:card_file_box:` | `raw` | Dados e parâmetros (por exemplo, os dados de exemplo) |
| 🧹 | `:broom:` | `cleanup` | Limpeza: código comentado, restos sem uso |
| 🗑️ | `:wastebasket:` | `remove` | Apagar ficheiros ou funcionalidades |
| 🔒️ | `:lock:` | `security` | Segurança: permissões, autenticação, dados expostos |
| 💥 | `:boom:` | `fix` | Desfazer mudanças de um commit anterior |

Exemplos:

```bash
git commit -m ":sparkles: feat(pedidos): aviso de pedidos parecidos" -m "Refs: EDS-169"
git commit -m ":bug: fix(contas): erro ao entrar sem email"
git commit -m ":books: docs(wiki): casos de uso por ator"
git commit -m ":bricks: ci(docker): postgresql no docker compose"
git commit -m ":test_tube: test(pedidos): voto repetido retira o voto"
```

Um commit faz uma coisa só. Se a mensagem precisa de "e" para juntar duas coisas diferentes, são dois commits.

## Ver também

- [Testes](testes.md)
- [AGENTS.md](../../AGENTS.md)
