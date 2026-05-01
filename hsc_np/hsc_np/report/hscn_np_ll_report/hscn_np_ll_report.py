import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_summary(data)

    return columns, data, None, None, summary


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Zone", "fieldname": "zone_name", "fieldtype": "Data", "width": 130},
        {"label": "Village", "fieldname": "village_name", "fieldtype": "Data", "width": 130},
        {"label": "House Owner", "fieldname": "house_owner_name", "fieldtype": "Data", "width": 150},
        {"label": "MDPE Pipe (mtr)", "fieldname": "mdpe_pipemtr", "fieldtype": "Int", "width": 130},
        {"label": "Samagra Id", "fieldname": "samagra_id", "fieldtype": "Data", "width": 130},
        {"label": "Aadhar Number", "fieldname": "aadhar_number", "fieldtype": "Data", "width": 130},
        {"label": "ElectroFusion Saddle", "fieldname": "electrofusion_saddle", "fieldtype": "Int", "width": 130},
        {"label": "Brass Ferrule", "fieldname": "brass_ferrule", "fieldtype": "Int", "width": 130},
        {"label": "FTA I Type", "fieldname": "int_kfob", "fieldtype": "Int", "width": 130},
        {"label": "FTA L Type", "fieldname": "fta_l_type", "fieldtype": "Int", "width": 130},
        {"label": "GI Socket", "fieldname": "gi_socket", "fieldtype": "Int", "width": 130},
        {"label": "GI Elbow", "fieldname": "gi_elbow", "fieldtype": "Int", "width": 130},
        {"label": "GI Nipple 9 Inch", "fieldname": "gi_nipple_nine", "fieldtype": "Int", "width": 130},
        {"label": "GI Nipple 30 Inch", "fieldname": "gi_nipple_thirty", "fieldtype": "Int", "width": 130},
        {"label": "Tap", "fieldname": "tap", "fieldtype": "Int", "width": 130},
        {"label": "Jointer", "fieldname": "jointer", "fieldtype": "Int", "width": 130},
        {"label": "Samagra Photo", "fieldname": "samagra_photo", "fieldtype": "HTML", "width": 150},
        {"label": "Aadhar Photo", "fieldname": "aadhar_photo", "fieldtype": "HTML", "width": 150},
        {"label": "Connection Photo", "fieldname": "connection_photo", "fieldtype": "HTML", "width": 150},
        {"label": "House Photo", "fieldname": "house_photo", "fieldtype": "HTML", "width": 150},
        {"label": "Latitude", "fieldname": "latitude", "fieldtype": "Float", "width": 130},
        {"label": "Longitude", "fieldname": "longitude", "fieldtype": "Float", "width": 130}
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]

    if filters.get("zone_name"):
        conditions += " AND zone_name = %(zone_name)s"
        values["zone_name"] = filters["zone_name"]

    if filters.get("village_name"):
        conditions += " AND village_name = %(village_name)s"
        values["village_name"] = filters["village_name"]

    return frappe.db.sql(f"""
        SELECT
            date,
            project,
            zone_name,
            village_name,
            house_owner_name,
            mdpe_pipemtr,
            jointer,
            tap,
            gi_nipple_nine,
            gi_nipple_thirty,
            gi_elbow,
            gi_socket,
            fta_l_type,
            int_kfob,
            brass_ferrule,
            electrofusion_saddle,
            aadhar_number,
            samagra_id,
            longitude,
            latitude,
			house_photo,connection_photo,samagra_photo,aadhar_photo
        FROM `tabHSC Inhouse NP-ll`
        WHERE docstatus < 2
        {conditions}
        ORDER BY date DESC
    """, values, as_dict=True)


def get_summary(data):
    total_mdpe = sum(flt(row.get("mdpe_pipemtr")) for row in data)

    return [
        {
            "label": "TOTAL MDPE PIPE USED (M)",
            "value": total_mdpe,
            "indicator": "Green"
        }
    ]