/** @odoo-module **/

// Odoo 18: algunos widgets monetarios usan utilidades numéricas base.
// Este parche fuerza 0 decimales para todo lo "currency", sin tocar otras cosas.

import * as numbers from "@web/core/utils/numbers";
import * as formatters from "@web/views/fields/formatters";
import { MonetaryField } from "@web/views/fields/monetary/monetary_field";

console.info("[money_no_cents_ui] parche activo v3");

// 1) Reencapsulamos los formateadores de campos (por si el widget los usa)
const _fmtMonetary = formatters.formatMonetary;
const _fmtFloat = formatters.formatFloat;

formatters.formatMonetary = (value, options = {}) =>
    _fmtMonetary(value, { ...options, digits: 0 });

formatters.formatFloat = (value, options = {}) =>
    _fmtFloat(value, { ...options, digits: 0 });

// 2) Forzamos 0 fracciones en el formateador numérico base si existe API dedicada
if (numbers.formatCurrency) {
    const _fmtCurrency = numbers.formatCurrency;
    numbers.formatCurrency = (value, currency, options = {}) => {
        return _fmtCurrency(value, currency, {
            ...options,
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        });
    };
}
if (numbers.formatNumber) {
    const _fmtNumber = numbers.formatNumber;
    numbers.formatNumber = (value, options = {}) => {
        const o = { ...options };
        if (o.style === "currency") {
            o.minimumFractionDigits = 0;
            o.maximumFractionDigits = 0;
        }
        return _fmtNumber(value, o);
    };
}

// 3) “Airbag” final: si algo llama directo a Intl.NumberFormat con style=currency
const _IntlNumberFormat = Intl.NumberFormat;
Intl.NumberFormat = function (locale, options = {}) {
    if (options && options.style === "currency") {
        options = { ...options, minimumFractionDigits: 0, maximumFractionDigits: 0 };
    }
    return new _IntlNumberFormat(locale, options);
};

// 4) Y, por si algún widget sigue usando el método de instancia:
const _oldFormat = MonetaryField.prototype.format;
MonetaryField.prototype.format = function (value) {
    // ignoramos cualquier precisión que calcule el widget
    return formatters.formatMonetary(value, {
        currency: this.props.currency,
        digits: 0,
    });
};
