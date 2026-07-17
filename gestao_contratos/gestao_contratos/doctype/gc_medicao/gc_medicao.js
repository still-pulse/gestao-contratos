// Copyright (c) 2026, StillPulse and contributors
// For license information, please see license.txt

frappe.ui.form.on("GC Medicao", {
	contrato(frm) {
		if (frm.doc.contrato && !(frm.doc.itens || []).length) {
			prefill_itens_from_contrato(frm);
		}
	},
});

frappe.ui.form.on("GC Item Medicao", {
	quantidade_executada(frm, cdt, cdn) {
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
	const total = flt(row.quantidade_executada) * flt(row.valor_unitario);
	frappe.model.set_value(cdt, cdn, "valor_calculado", total);
	recalc_total(frm);
}

function recalc_total(frm) {
	let sum = 0;
	(frm.doc.itens || []).forEach((row) => {
		sum += flt(row.valor_calculado);
	});
	frm.set_value("valor_total", sum);
}

function prefill_itens_from_contrato(frm) {
	frappe.db.get_doc("GC Contrato", frm.doc.contrato).then((doc) => {
		(doc.itens || []).forEach((item) => {
			const row = frm.add_child("itens");
			row.item_idx = item.idx;
			row.descricao = item.descricao;
			row.quantidade_executada = 0;
			row.valor_unitario = item.valor_unitario;
			row.valor_calculado = 0;
		});
		frm.refresh_field("itens");
	});
}
