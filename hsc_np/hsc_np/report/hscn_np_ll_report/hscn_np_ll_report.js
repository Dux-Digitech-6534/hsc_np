frappe.query_reports["HSCN NP ll Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.month_end()
        },
        {
            fieldname: "zone_name",
            label: "Zone",
            fieldtype: "Link",
            options: "Zone Details NP-ll"
        },
        {
            fieldname: "village_name",
            label: "Village",
            fieldtype: "Link",
            options: "Village Details NP-ll"
        }
    ],
	formatter(value, row, column, data, default_formatter) {

        const image_fields = [
        "house_photo",
        "connection_photo",
        "samagra_photo",
		"aadhar_photo"
        
       
    ];


        let file = data[column.fieldname];

        if (image_fields.includes(column.fieldname) && file) {

            let ext = file.split('.').pop().toLowerCase();

            if (["jpg", "jpeg", "png", "gif", "webp"].includes(ext)) {

                return `
                    <a href="${file}" target="_blank">
                        <img src="${file}" 
                             style="
                                height:40px;
                                width:40px;
                                object-fit:cover;
                                border-radius:4px;
                                border:1px solid #ccc;">
                    </a>`;
            }
        }

        return default_formatter(value, row, column, data);
},
onload(report) {
    setTimeout(() => {
        let summary = document.querySelector(".report-summary");
        if (summary) {
            summary.style.justifyContent = "flex-start";
            summary.style.textAlign = "left";
        }
    }, 300);
}
};