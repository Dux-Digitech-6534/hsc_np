frappe.ui.form.on('HSC Inhouse NP-ll', {

    refresh(frm) {

        apply_digit_validation(frm, "mobile_no", 10);
        // apply_digit_validation(frm, "samagra_id", 9);   // change length if needed
        apply_digit_validation(frm, "aadhar_number", 12);

    },

    validate(frm) {

        // Mobile number must be exactly 10 digits
        if (frm.doc.mobile_no && frm.doc.mobile_no.length != 10) {
            frappe.throw("Mobile Number must be exactly 10 digits.");
        }

        // Samagra ID length check
        // if (frm.doc.samagra_id && frm.doc.samagra_id.toString().length != 9) {
        //     frappe.throw("Samagra ID must be 9 digits.");
        // }

        // Aadhar length check
        if (frm.doc.aadhar_number && frm.doc.aadhar_number.length != 12) {
            frappe.throw("Aadhar Number must be 12 digits.");
        }

    }

});

// function apply_digit_validation(frm, fieldname, max_length) {

//     if (frm.fields_dict[fieldname] && frm.fields_dict[fieldname].$input) {

//         // Allow only digits while typing
//         frm.fields_dict[fieldname].$input.on('input', function () {
//             this.value = this.value.replace(/\D/g, ''); // remove non-digits
//             if (this.value.length > max_length) {
//                 this.value = this.value.slice(0, max_length);
//             }
//         });

//         // Allow paste but remove characters automatically
//         frm.fields_dict[fieldname].$input.on('paste', function (e) {
//             let pasted = (e.originalEvent || e).clipboardData.getData('text');
//             let cleaned = pasted.replace(/\D/g, '').slice(0, max_length);
//             e.preventDefault();
//             this.value = cleaned;
//         });

//     }
// }