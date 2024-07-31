/**
 * @param {String} text
 * @returns {Boolean}
 */

export function validateEmail(text) {
    return text?.indexOf("@") !== -1;
}

/**
 *
 * @param {String} password
 * @param {Integer} length
 * @returns {Boolean}
 */

export function validatePassword(password, length = 7) {
    return password?.length >= length;
}

/**
 *
 * @param {String} username
 * @returns {Boolean}
 */
export function validateUsername(username) {
    return /^[a-zA-Z0-9_-]+$/.test(username);
}

/**
 * @param {String} price
 * @return {Boolean}
 */
export function validatePrice(price) {
    return /^\d+\.\d{1,2}$/.test(String(price).trim());
}

export default {
    username: validateUsername,
    email: validateEmail,
    password: validatePassword,
    price: validatePrice
}