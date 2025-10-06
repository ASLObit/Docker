/** @odoo-module **/

import * as formatters from "@web/views/fields/formatters";
import { patch } from "@web/core/utils/patch";
import { MonetaryField } from "@web/views/fields/monetary/monetary_field";

console.info("[money_no_cents_ui] parche activo v2");

// Guardamos funciones originales
const _fmtMonetary = formatters.formatMonetary;
const _fmtFloat = formatters.formatFloat;

// Forzamos 0 decimales en formateadores (UI)
formatters.formatMonetary = (value, options = {}) =>
    _fmtMonetary(value, { ...options, digits: 0 });

formatters.formatFloat = (value, options = {}) =>
    _fmtFloat(value, { ...options, digits: 0 });

// Odoo 18 => patch(target, props)  (SIN el nombre intermedio)
patch(MonetaryField.prototype, {
    format(value) {
        return formatters.formatMonetary(value, {
            currency: this.props.currency,
            digits: 0,
        });
    },
});
