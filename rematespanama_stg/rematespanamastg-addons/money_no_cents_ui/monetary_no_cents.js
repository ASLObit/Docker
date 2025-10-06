/** @odoo-module **/
/*
  Fuerza a que todos los importes monetarios se muestren
  con 0 decimales (solo efecto visual).
*/
import * as formatters from "@web/core/formatters";

// Guardamos el formateador original
const _origFormatMonetary = formatters.formatMonetary;

/**
 * Reemplazo: inyecta digits=0 para mostrar sin decimales.
 * No cambia cálculos ni la moneda en BD; es solo la presentación.
 */
formatters.formatMonetary = function (value, options = {}) {
    const opts = { ...options, digits: 0 };
    return _origFormatMonetary(value, opts);
};
