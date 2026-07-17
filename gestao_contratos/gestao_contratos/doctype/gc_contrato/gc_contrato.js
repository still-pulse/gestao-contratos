// Copyright (c) 2026, StillPulse and contributors
// For license information, please see license.txt

frappe.ui.form.on("GC Contrato", {
	refresh(frm) {
		// placeholder for future actions
	},
});

frappe.ui.form.on("GC Item Contratual", {
	quantidade_prevista(frm, cdt, cdn) {
		recalc_item(frm, cdt, cdn);
	},
	valor_unitario(frm, cdt, cdn) {
		recalc_item(frm, cdt, cdn);
	},
	itens_remove(frm) {
		recalc_total(frm);
	},
});

function recalc_item(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const total = flt(row.quantidade_prevista) * flt(row.valor_unitario);
	frappe.model.set_value(cdt, cdn, "valor_total", total);
	recalc_total(frm);
}

function recalc_total(frm) {
	let sum = 0;
	(frm.doc.itens || []).forEach((row) => {
		sum += flt(row.valor_total);
	});
	frm.set_value("valor_itens_total", sum);
}
