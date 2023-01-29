/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername (str) {
  return str.trim().length > 0
}

/**
 * @param {string} value
 * @returns {Boolean}
 */
export function validPassword (value) {
  return value.length >= 6
}
