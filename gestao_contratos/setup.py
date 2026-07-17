# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

"""Pós-install / pós-migrate: roles e Workspace do módulo Axior."""

from __future__ import annotations

import frappe

ROLES = ("GC Gestor", "GC Operacional")
WORKSPACE_NAME = "Gestao Contratos"
MODULE_NAME = "Gestao Contratos"

DOCTYPES_LINKS = [
	"GC Contrato",
	"GC Aditivo",
	"GC Medicao",
	"GC Pagamento",
	"GC Penalidade",
]


def after_install():
	ensure_roles()
	ensure_workspace()
	frappe.db.commit()


def after_migrate():
	ensure_roles()
	ensure_workspace()
	frappe.db.commit()


def ensure_roles():
	for role in ROLES:
		if frappe.db.exists("Role", role):
			continue
		frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": role,
				"desk_access": 1,
				"is_custom": 1,
			}
		).insert(ignore_permissions=True)


def _workspace_content():
	blocks = [
		{"type": "header", "data": {"text": "Gestão de Contratos (Axior)", "col": 12}},
	]
	for dt in DOCTYPES_LINKS:
		if frappe.db.exists("DocType", dt):
			blocks.append(
				{
					"type": "shortcut",
					"data": {
						"shortcut_name": dt,
						"label": dt,
						"type": "DocType",
						"link_to": dt,
						"col": 4,
					},
				}
			)
	return blocks


def _workspace_links():
	rows = [{"type": "Card Break", "label": "Contratos e Lifecycle"}]
	for dt in DOCTYPES_LINKS:
		if frappe.db.exists("DocType", dt):
			rows.append(
				{
					"type": "Link",
					"label": dt,
					"link_type": "DocType",
					"link_to": dt,
				}
			)
	return rows


def ensure_workspace():
	"""Cria ou atualiza Workspace com atalhos dos DocTypes GC."""
	if not frappe.db.exists("DocType", "GC Contrato"):
		return

	content = _workspace_content()
	links = _workspace_links()

	if frappe.db.exists("Workspace", WORKSPACE_NAME):
		ws = frappe.get_doc("Workspace", WORKSPACE_NAME)
		ws.content = frappe.as_json(content)
		ws.links = []
		for row in links:
			ws.append("links", row)
		ws.flags.ignore_permissions = True
		ws.flags.ignore_links = True
		ws.save()
		return

	ws = frappe.get_doc(
		{
			"doctype": "Workspace",
			"name": WORKSPACE_NAME,
			"label": WORKSPACE_NAME,
			"title": WORKSPACE_NAME,
			"module": MODULE_NAME,
			"public": 1,
			"is_hidden": 0,
			"icon": "file",
			"content": frappe.as_json(content),
			"links": links,
		}
	)
	ws.insert(ignore_permissions=True)
