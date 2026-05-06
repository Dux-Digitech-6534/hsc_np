# import frappe
# from frappe.model.document import Document

# class HSCInhouseNPll(Document):

#     def after_insert(self):
#         self.create_material_issue()

#     def create_material_issue(self):
#         try:
#             company = frappe.defaults.get_user_default("Company")
#             company_abbr = frappe.get_value("Company", company, "abbr")
#             warehouse = self.hdi_contractor_name + " - " + company_abbr

#             stock_entry = frappe.new_doc("Stock Entry")
#             stock_entry.stock_entry_type = "Material Issue"
#             stock_entry.company = company

#             for item_code, qty in [
#                 ("MDPE Pipe", self.mdpe_pipemtr),
#                 ("ElectroFusion Saddle", self.electrofusion_saddle),
#                 ("Brass Ferrule", self.brass_ferrule),
#                 ("FTA I Type", self.fta_i_type),
#                 ("FTA L Type", self.fta_l_type),
#                 ("GI Socket", self.gi_socket),
#                 ("GI Elbow", self.gi_elbow),
#                 ("GI Nipple 9 Inch", self.gi_nipple_9_inch),
#                 ("GI Nipple 30 Inch", self.gi_nipple_30_inch),
#                 ("Tap", self.tap),
#                 ("Jointer", self.jointer),
#             ]:
#                 if qty and qty > 0:
#                     stock_entry.append("items", {
#                         "item_code": item_code,
#                         "qty": qty,
#                         "s_warehouse": warehouse,
#                         "allow_zero_valuation_rate": 1
#                     })

#             if not stock_entry.items:
#                 frappe.throw("No items found to issue!")

#             stock_entry.insert(ignore_permissions=True)
#             stock_entry.submit()

#             self.material_issue = stock_entry.name
#             self.db_update()

#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), "Material Issue Error - HSC NP-II")

#     def on_cancel(self):
#         if self.material_issue:
#             try:
#                 mi = frappe.get_doc("Stock Entry", self.material_issue)
#                 if mi.docstatus == 1:
#                     mi.cancel()
#             except Exception:
#                 frappe.log_error(frappe.get_traceback(), "HSC NP-II Cancel Sync Error")





# import frappe
# from frappe.model.document import Document

# class HSCInhouseNPll(Document):

#     def after_insert(self):
#         self.create_material_issue()

#     def create_material_issue(self):
#         try:
#             company = frappe.defaults.get_user_default("Company")
#             company_abbr = frappe.get_value("Company", company, "abbr")
#             warehouse = self.hdi_contractor_name + " - " + company_abbr

#             stock_entry = frappe.new_doc("Stock Entry")
#             stock_entry.stock_entry_type = "Material Issue"
#             stock_entry.company = company
#             # stock_entry.custom_hsc_reference = self.name

#             for item_code, qty in [
#                 ("MDPE Pipe (mtr)", self.mdpe_pipemtr),
#                 ("Brass Ferrule", self.brass_ferrule),
#                 ("FTA I Type", self.int_kfob),
#                 ("FTA - L", self.fta_l_type),
# 				("GL Socket", self.gi_socket),
# 				("GL Elbow", self.gi_elbow),
# 				("GL Nipple 9 inch", self.gi_nipple_nine),
# 				("GL Nipple 30 inch", self.gi_nipple_thirty),
#                 ("Tap", self.tap),
#                 ("Jointer", self.jointer),
#             ]:
#                 if qty and qty > 0:
#                     stock_entry.append("items", {
#                         "item_code": item_code,
#                         "qty": qty,
#                         "s_warehouse": warehouse,
#                         "allow_zero_valuation_rate": 1
#                     })

#             if not stock_entry.items:
#                 frappe.throw("No items found to issue")

#             stock_entry.insert(ignore_permissions=True)
#             stock_entry.submit()

#             self.material_issue = stock_entry.name
#             self.db_update()

#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), "Material Issue Creation Error")

#     def on_cancel(self):
#         if self.material_issue:
#             try:
#                 mi = frappe.get_doc("Stock Entry", self.material_issue)
#                 if mi.docstatus == 1:
#                     mi.cancel()
#             except Exception:
#                 frappe.log_error(frappe.get_traceback(), "HSC NP-II Cancel Sync Error")
                
                
                
                
                
                
                
                
                

import frappe
from frappe.model.document import Document

class HSCInhouseNPll(Document):

    def after_insert(self):
        self.create_material_issue()

    def create_material_issue(self):
        try:
            company = frappe.defaults.get_user_default("Company")
            company_abbr = frappe.get_value("Company", company, "abbr")
            warehouse = self.hdi_contractor_name + " - " + company_abbr

            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.stock_entry_type = "Material Issue"
            stock_entry.company = company

            for item_code, qty in [
                ("MDPE Pipe (mtr)", self.mdpe_pipemtr),
                ("Brass Ferrule", self.brass_ferrule),
                ("FTA-I", self.int_kfob),          # ✅ Fixed
                ("FTA - L", self.fta_l_type),
                ("GI Socket", self.gi_socket),      # ✅ Fixed (GL → GI)
                ("GI Elbow", self.gi_elbow),        # ✅ Fixed (GL → GI)
                ("GI Nipple 9 inch", self.gi_nipple_nine),   # ✅ Fixed (GL → GI)
                ("GI Nipple 30 inch", self.gi_nipple_thirty), # ✅ Fixed (GL → GI)
                ("Tap", self.tap),
                ("Jointer", self.jointer),
            ]:
                if qty and qty > 0:
                    stock_entry.append("items", {
                        "item_code": item_code,
                        "qty": qty,
                        "s_warehouse": warehouse,
                        "allow_zero_valuation_rate": 1
                    })

            if not stock_entry.items:
                frappe.throw("No items found to issue")

            stock_entry.insert(ignore_permissions=True)
            stock_entry.submit()

            self.material_issue = stock_entry.name
            self.db_update()

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Material Issue Creation Error")

    def on_cancel(self):
        if self.material_issue:
            try:
                mi = frappe.get_doc("Stock Entry", self.material_issue)
                if mi.docstatus == 1:
                    mi.cancel()
            except Exception:
                frappe.log_error(frappe.get_traceback(), "HSC NP-II Cancel Sync Error")