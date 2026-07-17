// Copyright (c) 2026, StillPulse and contributors
// For license information, please see license.txt

frappe.ui.form.on("GC Pagamento", {
	setup(frm) {
		frm.set_query("medicao", function () {
			return {
				filters: {
					contrato: frm.doc.contrato || "",
				},
			};
		});
	},
	medicao(frm) {
		if (!frm.doc.medicao) return;
		frappe.db.get_value("GC Medicao", frm.doc.medicao, ["contrato", "valor_total"]).then((r) => {
			if (!r.message) return;
			if (r.message.contrato && !frm.doc.contrato) {
				frm.set_value("contrato", r.message.contrato);
			}
			if (r.message.valor_total && !frm.doc.valor) {
				frm.set_value("valor", r.message.valor_total);
			}
		});
	},
});
