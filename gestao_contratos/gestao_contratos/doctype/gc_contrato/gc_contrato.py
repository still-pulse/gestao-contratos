# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class GCContrato(Document):
	def validate(self):
		self._validate_dates()
		self._calculate_itens()

	def _validate_dates(self):
		if self.data_inicio and self.data_fim:
			if getdate(self.data_fim) < getdate(self.data_inicio):
				frappe.throw(_("Data Fim não pode ser anterior à Data Início."))

	def _calculate_itens(self):
		total = 0.0
		for row in self.get("itens") or []:
			qty = flt(row.quantidade_prevista)
			rate = flt(row.valor_unitario)
			row.valor_total = flt(qty * rate, 2)
			total += flt(row.valor_total)
		self.valor_itens_total = flt(total, 2)
