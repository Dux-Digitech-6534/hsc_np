


                
                
                
                
                
# this is the main code of 15/5/26 

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
#                 ("MDPE Pipe (mtr)", self.mdpe_pipemtr),
#                 ("Brass Ferrule", self.brass_ferrule),
#                 ("FTA-I", self.int_kfob),          # ✅ Fixed
#                 ("FTA - L", self.fta_l_type),
#                 ("GI Socket", self.gi_socket),      # ✅ Fixed (GL → GI)
#                 ("GI Elbow", self.gi_elbow),        # ✅ Fixed (GL → GI)
#                 ("GI Nipple 9 inch", self.gi_nipple_nine),   # ✅ Fixed (GL → GI)
#                 ("GI Nipple 30 inch", self.gi_nipple_thirty), # ✅ Fixed (GL → GI)
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




# MAIN CODE OF 18/5/26 

# import frappe
# from frappe.model.document import Document


# class HSCInhouseNPll(Document):

#     def on_submit(self):
#         self.create_material_issue()

#     def create_material_issue(self):
#         try:
#             # Duplicate Material Issue create na ho
#             if self.material_issue:
#                 return

#             company = frappe.defaults.get_user_default("Company")
#             if not company:
#                 frappe.throw("Default Company not found for current user")

#             company_abbr = frappe.get_value("Company", company, "abbr")
#             if not company_abbr:
#                 frappe.throw(f"Company abbreviation not found for company {company}")

#             if not self.hdi_contractor_name:
#                 frappe.throw("Contractor Name is required to find source warehouse")

#             warehouse = self.hdi_contractor_name + " - " + company_abbr

#             if not frappe.db.exists("Warehouse", warehouse):
#                 frappe.throw(f"Source Warehouse not found: {warehouse}")

#             stock_entry = frappe.new_doc("Stock Entry")
#             stock_entry.stock_entry_type = "Material Issue"
#             stock_entry.company = company

#             items = [
#                 ("MDPE Pipe (mtr)", self.mdpe_pipemtr),
#                 ("Brass Ferrule", self.brass_ferrule),
#                 ("FTA-I", self.int_kfob),
#                 ("FTA - L", self.fta_l_type),
#                 ("GI Socket", self.gi_socket),
#                 ("GI Elbow", self.gi_elbow),
#                 ("GI Nipple 9 inch", self.gi_nipple_nine),
#                 ("GI Nipple 30 inch", self.gi_nipple_thirty),
#                 ("Tap", self.tap),
#                 ("Jointer", self.jointer),
#             ]

#             for item_code, qty in items:
#                 if qty and qty > 0:
#                     if not frappe.db.exists("Item", item_code):
#                         frappe.throw(f"Item not found: {item_code}")

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

#             # Existing ERP Connection tab wali Material Issue field me ID set karega
#             self.db_set("material_issue", stock_entry.name, update_modified=False)

#         except Exception:
#             frappe.log_error(
#                 frappe.get_traceback(),
#                 "Material Issue Creation Error"
#             )
#             frappe.throw("Material Issue create karte time error aaya. Error Log check karo.")

#     def on_cancel(self):
#         if self.material_issue:
#             try:
#                 mi = frappe.get_doc("Stock Entry", self.material_issue)
#                 if mi.docstatus == 1:
#                     mi.cancel()

#             except Exception:
#                 frappe.log_error(
#                     frappe.get_traceback(),
#                     "HSC NP-II Cancel Sync Error"
#                 )
#                 frappe.throw("Linked Material Issue cancel karte time error aaya. Error Log check karo.")
                
                
                
                
                
                
                
                
import frappe
from frappe.model.document import Document


class HSCInhouseNPll(Document):

    def validate(self):
        self.validate_exact_digits()

    def validate_exact_digits(self):
        rules = {
            "mobile_no": 10,
            "samagra_id": 9,
            "aadhar_number": 12,
        }

        labels = {
            "mobile_no": "Mobile No",
            "samagra_id": "Samagra ID",
            "aadhar_number": "Aadhar Number",
        }

        for fieldname, exact_length in rules.items():
            value = self.get(fieldname)

            if not value:
                continue

            value = str(value).strip()

            if not value.isdigit():
                frappe.throw(f"{labels[fieldname]} me sirf number allowed hai")

            if len(value) != exact_length:
                frappe.throw(
                    f"{labels[fieldname]} exactly {exact_length} digit ka hona chahiye"
                )

    def on_submit(self):
        self.create_material_issue()

    def create_material_issue(self):
        try:
            # Duplicate Material Issue create na ho
            if self.material_issue:
                return

            company = frappe.defaults.get_user_default("Company")
            if not company:
                frappe.throw("Default Company not found for current user")

            company_abbr = frappe.get_value("Company", company, "abbr")
            if not company_abbr:
                frappe.throw(f"Company abbreviation not found for company {company}")

            if not self.hdi_contractor_name:
                frappe.throw("Contractor Name is required to find source warehouse")

            warehouse = self.hdi_contractor_name + " - " + company_abbr

            if not frappe.db.exists("Warehouse", warehouse):
                frappe.throw(f"Source Warehouse not found: {warehouse}")

            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.stock_entry_type = "Material Issue"
            stock_entry.company = company

            items = [
                ("MDPE Pipe (mtr)", self.mdpe_pipemtr),
                ("Brass Ferrule", self.brass_ferrule),
                ("FTA-I", self.int_kfob),
                ("FTA - L", self.fta_l_type),
                ("GI Socket", self.gi_socket),
                ("GI Elbow", self.gi_elbow),
                ("GI Nipple 9 inch", self.gi_nipple_nine),
                ("GI Nipple 30 inch", self.gi_nipple_thirty),
                ("Tap", self.tap),
                ("Jointer", self.jointer),
            ]

            for item_code, qty in items:
                if qty and qty > 0:
                    if not frappe.db.exists("Item", item_code):
                        frappe.throw(f"Item not found: {item_code}")

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

            # Existing ERP Connection tab wali Material Issue field me ID set karega
            self.db_set("material_issue", stock_entry.name, update_modified=False)

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Material Issue Creation Error"
            )
            frappe.throw("Material Issue create karte time error aaya. Error Log check karo.")

    def on_cancel(self):
        if self.material_issue:
            try:
                mi = frappe.get_doc("Stock Entry", self.material_issue)
                if mi.docstatus == 1:
                    mi.cancel()

            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    "HSC NP-II Cancel Sync Error"
                )
                frappe.throw("Linked Material Issue cancel karte time error aaya. Error Log check karo.")
                
                
                
                
