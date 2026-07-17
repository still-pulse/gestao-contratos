# SPEC — gestao_contratos (Axior → ERPNext)

| | |
|---|---|
| **Versão** | 0.3.0 |
| **Ambiente** | gregory-dev (ERPNext 15) |
| **Fonte de regras** | Axior (Lovable/Supabase) — funcionalidades, não UI |
| **App** | `gestao_contratos` |
| **Não confundir** | App `contratos` (BHCL / PRD regimental) |

---

## 1. Princípios

1. Desk nativo (Form / List / Workspace / Report). Sem SPA React.
2. Nomes técnicos de DocType em **ASCII** (prefixo `GC ` para isolar do app BHCL).
3. Reusar ERPNext quando couber: `Supplier`, `Company`, `Project`, `UOM`, `Item` (opcional depois).
4. Sem multitenancy SaaS (`ltree` / RLS). Isolamento via Company + User Permission se necessário.
5. Implementação por fatias P0 → P1 → P2.

---

## 2. Mapa Axior → ERPNext

### P0 — núcleo (em implementação)

| Axior | DocType / nativo | Tipo | Status |
|---|---|---|---|
| `contracts` | **GC Contrato** | DocType | **Feito (0.2)** |
| `itens_contratuais` | **GC Item Contratual** | Child Table | **Feito (0.2)** |
| `projects` | `Project` (ERPNext) | Nativo + link | **Feito (0.2)** |
| unidade / tenant | `Company` | Nativo + link | **Feito (0.2)** |
| contratado (pessoa PJ) | `Supplier` | Nativo + link | **Feito (0.2)** |
| `aditivos_contrato` | **GC Aditivo** | DocType | **Feito (0.3)** |
| `medicoes` + `medicoes_itens` | **GC Medicao** + **GC Item Medicao** | DocType | **Feito (0.3)** |
| `pagamentos` | **GC Pagamento** | DocType | **Feito (0.3)** |
| `penalidades` | **GC Penalidade** | DocType | **Feito (0.3)** |

### P1 — pessoas e protocolo

| Axior | Destino | Notas |
|---|---|---|
| `pessoas` PF/PJ | Supplier/Customer + Contact/Address ou **GC Pessoa** | Decidir após P0 |
| categorias / docs / contatos | child tables ou nativos | |
| `expedientes` | **GC Expediente** | |
| `expediente_tipos` | **GC Tipo Expediente** | |

### P2 — acompanhamento e docs

| Axior | Destino |
|---|---|
| `timelines` | **GC Timeline** |
| `documents` / templates | Print Format + **GC Documento** (se precisar) |
| dashboard / stats | Workspace + Number Card |
| CNPJ/CNES | reusar `busca_cnpj` se instalado |

### Fora de escopo

- Frontend Vite/React/shadcn do Axior  
- Supabase Auth / RLS / Edge Functions como destino  
- Multitenancy Grupo→Projeto→Unidade com `ltree`  
- Fluxo regimental BHCL (RS → Cotação → OS → Instrumento) — app `contratos`  

---

## 3. Fluxo P0 (usuário)

```
Company (unidade) + Supplier (contratado) [+ Project opcional]
        │
        ▼
   GC Contrato  ──child──► GC Item Contratual (N)
        │
        ├──► GC Aditivo (N)          [slice 2]
        ├──► GC Medicao (N)          [slice 2]
        │         └── itens medidos
        ├──► GC Pagamento (N)        [slice 2]
        └──► GC Penalidade (N)       [slice 2]
```

---

## 4. GC Contrato — campos (slice 1)

Mapeamento Axior `contracts` + UI types:

| Campo Frappe | Tipo | Axior | Obrig. | Notas |
|---|---|---|---|---|
| `naming_series` | Select | — | sim | `GC-CONT-.YYYY.-.#####` |
| `company` | Link Company | unidade / tenant | sim | Contratante |
| `project` | Link Project | projeto_id | não | |
| `supplier` | Link Supplier | contratado_id | sim | Contratada |
| `objeto` | Small Text | objeto | sim | |
| `tipo_preco` | Select | tipo_preco | sim | `Fixo` / `Variavel` |
| `valor_mensal` | Currency | valor_mensal | não | |
| `data_inicio` | Date | data_inicio | sim | |
| `data_fim` | Date | data_fim | sim | validate ≥ início |
| `status` | Select | status | sim | `Rascunho`, `Vigente`, `Vencido`, `Suspenso`, `Cancelado` |
| `observacoes` | Text | observacoes | não | |
| `itens` | Table | itens_contratuais | não | child |
| `valor_itens_total` | Currency | (calc) | — | soma linhas, read only |

### GC Item Contratual (child)

| Campo | Tipo | Axior |
|---|---|---|
| `descricao` | Data/Small Text | descricao |
| `unidade_medida` | Data | unidade (Unidade, Horas, M²…) |
| `quantidade_prevista` | Float | quantidade_prevista |
| `valor_unitario` | Currency | valor_unitario |
| `valor_total` | Currency | calc qty × unitário |
| `observacoes` | Small Text | observacoes |

### Regras (controller)

1. `data_fim` ≥ `data_inicio`  
2. Em cada item: `valor_total = quantidade_prevista * valor_unitario`  
3. `valor_itens_total = sum(itens.valor_total)`  

---

## 5. Slices seguintes (P0 restante)

### Slice 2 — lifecycle (**feito em 0.3.0**)

- **GC Aditivo**: numero, tipo (Valor/Prazo/Escopo/Outros), valores/prazos, data_assinatura, status  
- **GC Medicao**: periodo, data, aprovada, % físico, valor_total; child **GC Item Medicao** (prefill a partir do contrato)  
- **GC Pagamento**: valor, vencimento, pagamento, tipo/numero documento, competencia, link medicao (validado)  
- **GC Penalidade**: tipo, valor, data, motivo, status  

### Slice 3 — UX P0 / polish

- Roles já criadas: `GC Gestor`, `GC Operacional`  
- Workspace com atalhos (atualizado no migrate)  
- Alertas de vencimento (scheduler) — opcional  
- Dashboard Number Cards — opcional  

### Critério de pronto — Slice 2

- [x] DocTypes no filesystem  
- [ ] migrate no gregory-dev  
- [ ] Connections no form GC Contrato  


---

## 6. Convenções técnicas

- Módulo Frappe: `Gestao Contratos`  
- Controllers em `gestao_contratos/gestao_contratos/doctype/...`  
- `after_migrate` / `after_install`: garantir Workspace  
- Cada release: commit + **tag** semântica  
- Deploy: hot-deploy no gregory-dev + `migrate` + restart workers  

---

## 7. Critério de pronto — Slice 1

- [x] SPEC neste arquivo  
- [x] DocTypes `GC Contrato` e `GC Item Contratual` no filesystem  
- [x] migrate no gregory-dev sem erro (`v0.2.0`)  
- [ ] Criar/editar contrato com itens no Desk (validação manual)  
- [x] Workspace **Gestao Contratos** criado no site  

