/** @odoo-module **/

/*
  Fuerza a que TODOS los importes monetarios se muestren con 0 decimales.
  - Parchea los formatters globales (formatMonetary, formatFloat)
  - Parchea el widget MonetaryField por si algún lugar lo invoca directo
  - Deja un console.info para verificar que el asset se cargó
*/

import * as formatters from "@web/core/formatters";
import { patch } from "@web/core/utils/patch";
import { MonetaryField } from "@web/views/fields/monetary/monetary_field";

console.info("[money_no_cents_ui] parche de formateo monetario activo");

// 1) Guardamos originales
const _origFormatMonetary = formatters.formatMonetary;
const _origFormatFloat = formatters.formatFloat;

// 2) Parcheamos: siempre digits=0 (solo UI; no cambia cálculos)
formatters.formatMonetary = function (value, options = {}) {
    const opts = { ...options, digits: 0 };
    return _origFormatMonetary(value, opts);
};

formatters.formatFloat = function (value, options = {}) {
    // Por si algún widget usa formatFloat para mostrar moneda
    const opts = { ...options, digits: 0 };
    return _origFormatFloat(value, opts);
};

// 3) “Cinturón y tirantes”: aseguramos que el widget monetario
//    también renderice con 0 decimales aunque pase currency con otros digits.
patch(MonetaryField.prototype, "money_no_cents_ui.patch", {
    format(value) {
        return formatters.formatMonetary(value, {
            currency: this.props.currency,
            digits: 0,
        });
    },
});
