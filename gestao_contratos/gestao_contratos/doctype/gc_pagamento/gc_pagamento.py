# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class GCPagamento(Document):
	def validate(self):
		if self.medicao and self.contrato:
			med_contrato = frappe.db.get_value("GC Medicao", self.medicao, "contrato")
			if med_contrato and med_contrato != self.contrato:
				frappe.throw(_("A Medição selecionada não pertence a este Contrato."))
