# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class GCAditivo(Document):
	def validate(self):
		if self.tipo == "Prazo" and self.prazo_anterior and self.prazo_novo:
			if getdate(self.prazo_novo) < getdate(self.prazo_anterior):
				frappe.throw(_("Prazo Novo não pode ser anterior ao Prazo Anterior."))
		if self.tipo == "Valor" and self.valor_novo is not None and self.valor_anterior is not None:
			# apenas informativo — não bloqueia redução
			pass
