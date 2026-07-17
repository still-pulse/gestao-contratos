# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

"""Pós-install / pós-migrate: roles e Workspace do módulo Axior."""

from __future__ import annotations

import frappe

ROLES = ("GC Gestor", "GC Operacional")
WORKSPACE_NAME = "Gestao Contratos"
MODULE_NAME = "Gestao Contratos"


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


def ensure_workspace():
	"""Cria Workspace com atalho para GC Contrato (idempotente)."""
	if not frappe.db.exists("DocType", "GC Contrato"):
		return

	if frappe.db.exists("Workspace", WORKSPACE_NAME):
		return

	content = [
		{"type": "header", "data": {"text": "Gestão de Contratos (Axior)", "col": 12}},
		{
			"type": "shortcut",
			"data": {
				"shortcut_name": "GC Contrato",
				"label": "GC Contrato",
				"type": "DocType",
				"link_to": "GC Contrato",
				"col": 4,
			},
		},
	]

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
			"links": [
				{"type": "Card Break", "label": "Contratos"},
				{
					"type": "Link",
					"label": "GC Contrato",
					"link_type": "DocType",
					"link_to": "GC Contrato",
				},
			],
		}
	)
	ws.insert(ignore_permissions=True)
