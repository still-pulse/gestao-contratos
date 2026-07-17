# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt


class GCMedicao(Document):
	def validate(self):
		self._calculate_itens()

	def _calculate_itens(self):
		total = 0.0
		for row in self.get("itens") or []:
			qty = flt(row.quantidade_executada)
			rate = flt(row.valor_unitario)
			row.valor_calculado = flt(qty * rate, 2)
			total += flt(row.valor_calculado)
		self.valor_total = flt(total, 2)
