// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Component', {
	setup: function(frm) {
		frm.set_query("default_account", "accounts", function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			var root_types = ["Expense", "Liability"];
			return {
				filters: {
					"root_type": ["in", root_types],
					"is_group": 0,
					"company": d.company
				}
			};
		});
		frm.set_query("earning_component_group", function() {
			return {
				filters: {
					"is_group": 1,
					"is_flexible_benefit": 1
				}
			};
		});
	},
	is_flexible_benefit: function(frm) {
		if(frm.doc.is_flexible_benefit){
			set_value_for_condition_and_formula(frm);
			frm.set_value("is_additional_component", 0);
		}
	},
	is_additional_component: function(frm) {
		if(frm.doc.is_additional_component){
			frm.set_value("is_flexible_benefit", 0);
		}
	},
	type: function(frm) {
		if(frm.doc.type=="Earning"){
			frm.set_value("is_tax_applicable", 1);
			frm.set_value("variable_based_on_taxable_salary", 0);
		}
		if(frm.doc.type=="Deduction"){
			frm.set_value("is_tax_applicable", 0);
			frm.set_value("is_flexible_benefit", 0);
		}
	},
	variable_based_on_taxable_salary: function(frm) {
		if(frm.doc.variable_based_on_taxable_salary){
			set_value_for_condition_and_formula(frm);
		}
	},
	create_separate_payment_entry_against_benefit_claim: function(frm) {
		if(frm.doc.create_separate_payment_entry_against_benefit_claim){
			frm.set_df_property("accounts", "reqd", 1);
		}
		else{
			frm.set_df_property("accounts", "reqd", 0);
		}
	}
});

var set_value_for_condition_and_formula = function(frm) {
	frm.set_value("formula", null);
	frm.set_value("condition", null);
	frm.set_value("amount_based_on_formula", 0);
	frm.set_value("statistical_component", 0);
	frm.set_value("do_not_include_in_total", 0);
	frm.set_value("depends_on_lwp", 0);
};
