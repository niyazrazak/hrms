# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

test_records = frappe.get_test_records('Expense Claim')

class TestExpenseClaim(unittest.TestCase):
	def test_project_costing(self):
		frappe.db.sql("delete from `tabTask`")
		frappe.db.sql("delete from `tabProject`")
		
		frappe.get_doc({
			"project_name": "_Test Project 1",
			"doctype": "Project",
			"tasks" :
				[{ "title": "_Test Project Task 1", "status": "Open" }]
		}).save()
		
		task_name = frappe.db.get_value("Task",{"project": "_Test Project 1"})
		expense_claim = frappe.get_doc({
			 "doctype": "Expense Claim",
			 "employee": "_T-Employee-0001",
			 "posting_date": "2015-07-07",
			 "fiscal_year": "_Test Fiscal Year 2015",
			 "approval_status": "Approved",
			 "project": "_Test Project 1",
			 "task": task_name,
			 "expenses": 
			 	[{ "expense_type": "Food", "claim_amount": 300, "sanctioned_amount": 200 }]
		})
		expense_claim.submit()
		
		self.assertEqual(frappe.db.get_value("Task", task_name, "total_expense_claim"), 200)
		self.assertEqual(frappe.db.get_value("Project", "_Test Project 1", "total_expense_claim"), 200)
		
		expense_claim2 = frappe.get_doc({
			 "doctype": "Expense Claim",
			 "employee": "_T-Employee-0001",
			 "posting_date": "2015-07-07",
			 "approval_status": "Approved",
			 "project": "_Test Project 1",
			 "task": task_name,
			 "expenses": 
			 	[{ "expense_type": "Food", "claim_amount": 600, "sanctioned_amount": 500 }]
		})
		expense_claim2.submit()
		
		self.assertEqual(frappe.db.get_value("Task", task_name, "total_expense_claim"), 700)
		self.assertEqual(frappe.db.get_value("Project", "_Test Project 1", "total_expense_claim"), 700)
		
		expense_claim2.cancel()
		
		self.assertEqual(frappe.db.get_value("Task", task_name, "total_expense_claim"), 200)
		self.assertEqual(frappe.db.get_value("Project", "_Test Project 1", "total_expense_claim"), 200)
