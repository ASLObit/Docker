/** @odoo-module **/

// 👈 paths correctos para Odoo 18
import * as formatters from "@web/views/fields/formatters";
import { patch } from "@web/core/utils/patch";
import { MonetaryField } from "@web/views/fields/monetary/monetary_field";

console.info("[money_no_cents_ui] parche activo");

// Guardamos referencias originales
const _origFormatMonetary = formatters.formatMonetary;
const _origFormatFloat = formatters.formatFloat;

// Forzamos 0 decimales en los formateadores (UI)
formatters.formatMonetary = function (value, options = {}) {
    return _origFormatMonetary(value, { ...options, digits: 0 });
};
formatters.formatFloat = function (value, options = {}) {
    return _origFormatFloat(value, { ...options, digits: 0 });
};

// Y también en el widget Monetary (listas/ formularios)
patch(MonetaryField.prototype, "money_no_cents_ui.patch", {
    format(value) {
        return formatters.formatMonetary(value, {
            currency: this.props.currency,
            digits: 0,
        });
    },
});
