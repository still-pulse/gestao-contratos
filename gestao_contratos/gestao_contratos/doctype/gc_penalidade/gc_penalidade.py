# Copyright (c) 2026, StillPulse and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class GCPenalidade(Document):
	def validate(self):
		if self.tipo == "Multa" and flt(self.valor) <= 0:
			frappe.throw(_("Penalidade do tipo Multa deve ter valor maior que zero."))
