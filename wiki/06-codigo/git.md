# Git e pull requests

[Índice](../README.md) · [← Testes](testes.md) · [Equipa e papéis →](../07-scrum/equipa-e-papeis.md)

- Há uma branch principal, a `main`.
- Cada cartão do Jira tem a sua branch: `feature/EDS-164-ambiente`.
- Cada pessoa faz commit do seu próprio trabalho, com a sua conta. É o histórico do Git que mostra quem fez o quê.
- Mensagens de commit curtas, em português, com um prefixo: `feat:`, `fix:`, `test:`, `docs:`, `chore:`. Exemplo: `feat: aviso de pedidos parecidos no novo pedido`.
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

## Ver também

- [Testes](testes.md)
- [AGENTS.md](../../AGENTS.md)
