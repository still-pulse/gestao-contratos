# gestao_contratos

App Frappe/ERPNext **v15** — port das **funcionalidades** do [Axior](https://axior.app) (Lovable/Supabase) para o **Desk nativo** do ERPNext.

| | |
|---|---|
| **Repo** | https://github.com/still-pulse/gestao-contratos |
| **App name** | `gestao_contratos` |
| **Módulo** | Gestao Contratos |
| **Ambiente de dev** | `gregory-dev` (VPS Dokploy) — ERPNext 15 |
| **UI** | Desk nativo (Form / List / Workspace). **Não** reutiliza o frontend React do Axior. |

> **Não confundir** com o app [`contratos`](https://github.com/still-pulse/contratos) (módulo regimental BHCL: RS → Cotação → OS → Instrumento). Este repositório é **somente** o domínio Axior.

---

## Escopo

Funcionalidades de referência no Axior:

- Projetos e unidades
- Contratos (aditivos, itens, medições, pagamentos, penalidades)
- Pessoas (PF/PJ, categorias, contatos, documentos)
- Expedientes (recebidos/enviados) e timelines
- Documentos / templates / PDF
- Papéis e permissões (remodelados em Roles Frappe)

Multitenancy SaaS (`ltree` + RLS Supabase) **não** é objetivo neste app: no ERPNext usamos Company / User Permission conforme necessidade do site.

---

## Instalação (bench / gregory-dev)

O repositório GitHub usa hífen (`gestao-contratos`); o pacote Python e o app name usam underscore (`gestao_contratos`). Clone **sempre** para a pasta com underscore:

```bash
cd /home/frappe/frappe-bench/apps
git clone https://github.com/still-pulse/gestao-contratos.git gestao_contratos
cd /home/frappe/frappe-bench
./env/bin/pip install -e apps/gestao_contratos

# Registrar o app no bench (necessário se não usou get-app)
grep -qx gestao_contratos sites/apps.txt || echo gestao_contratos >> sites/apps.txt

bench --site frontend install-app gestao_contratos
bench --site frontend migrate
bench --site frontend clear-cache
```

Hot-deploy no **gregory-dev**: copiar/clonar em **todos** os containers Frappe (`backend`, `queue-*`, `scheduler`, `websocket`), `pip install -e` em cada um, depois `install-app` só no backend.

Ou, se `bench get-app` estiver disponível e renomear corretamente:

```bash
bench get-app https://github.com/still-pulse/gestao-contratos.git --branch main
# se a pasta ficar gestao-contratos, renomear:
# mv apps/gestao-contratos apps/gestao_contratos
bench --site frontend install-app gestao_contratos
```

### Dependências

- Frappe / ERPNext **v15**
- Opcional: `busca_cnpj` (consulta CNPJ no site BHCL/gregory-dev)

---

## Matriz Axior → DocTypes (planejamento)

Nomes técnicos **ASCII** (sem acento no `name` do DocType). Labels na UI podem ter acento.

### P0 — núcleo contratual (MVP)

| Capacidade Axior | DocType técnico (proposto) | Notas |
|---|---|---|
| Projeto | `GC Projeto` ou reusar `Project` | Preferir nativo + campos custom se bastar |
| Unidade | `Company` / `Cost Center` ou `GC Unidade` | Avaliar na implementação |
| Contrato | `GC Contrato` | Hub consolidado |
| Itens contratuais | `GC Item Contratual` (child) | Planilha de quantitativos |
| Aditivo | `GC Aditivo` | Valor / prazo / escopo |
| Medição | `GC Medicao` + child itens | Acompanhamento de execução |
| Pagamento | `GC Pagamento` | Cronograma / quitação |
| Penalidade | `GC Penalidade` | Sanções contratuais |
| Fornecedor / contratado | `Supplier` (+ campos) | Reusar ERPNext + `busca_cnpj` |

### P1 — pessoas e protocolo

| Capacidade Axior | DocType técnico (proposto) | Notas |
|---|---|---|
| Pessoa unificada PF/PJ | `GC Pessoa` ou Supplier/Customer | Unificar cadastro rico do Axior |
| Categorias de pessoa | `GC Categoria Pessoa` | Configurável |
| Contatos / endereços / docs | child tables ou Contact/Address | Preferir nativos quando possível |
| Expediente | `GC Expediente` | Recebido / enviado |
| Tipo de expediente | `GC Tipo Expediente` | Cadastro admin |

### P2 — acompanhamento e documentos

| Capacidade Axior | DocType técnico (proposto) | Notas |
|---|---|---|
| Timeline | `GC Timeline` | Agrupa expedientes |
| Documentos / templates | `GC Documento` / Print Format | Editor rich freeform = Print Format |
| Dashboard estatístico | Workspace + Number Card | Sem SPA React |
| Busca global | Desk Awesomebar + reports | — |

### Fora de escopo (por enquanto)

| Axior | Motivo |
|---|---|
| Multitenancy Grupo→Projeto→Unidade com `ltree` | Modelo SaaS; ERPNext usa Company/permissions |
| Frontend Vite/React/shadcn | UI remodelada no Desk |
| Supabase Auth / RLS / Edge Functions | Auth e permissões Frappe |

---

## Estrutura do app

```
gestao_contratos/
├── hooks.py
├── modules.txt          # Gestao Contratos
├── patches.txt
├── config/
├── patches/
├── templates/
└── gestao_contratos/    # módulo (scrub de "Gestao Contratos")
    └── doctype/         # DocTypes entram aqui
```

---

## Versão

`0.3.0` — P0 completo (slice 1 + 2):

- **GC Contrato** + **GC Item Contratual**
- **GC Aditivo**, **GC Medicao** (+ **GC Item Medicao**), **GC Pagamento**, **GC Penalidade**
- Workspace **Gestao Contratos** com atalhos

Ver `docs/SPEC.md`.

## Licença

MIT — StillPulse
