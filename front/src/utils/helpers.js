/**
 * Returns an object value or default value if undefined
 * @param {*} arg object
 * @param {*} value default value
 * @param {boolean} [isNullable=false] indicates whether the value can be assigned the value *NULL*
 */
export function valOrDefault(arg, value, isNullable = false) {
    if (isNullable) {
        return isUndefined(arg) ? value : arg;
    }

    return isNullOrUndefined(arg) ? value : arg;
}

/**
 * Returns a value indicating whether the value is empty
 * @param {Object[]|string} arr array
 * @returns {boolean}
 */
export function isEmpty(obj) {
    return isIterable(obj) && obj.length === 0;
}

/**
 * Returns a value indicating whether the variable is a Date
 * @param {*} value 
 * @returns {boolean}
 */
export function isDate(value) {
    return value instanceof Date || (typeof value === 'object' && Object.prototype.toString.call(value) === '[object Date]');
}

/**
 * Returns a value indicating whether the variable is a String
 * @param {*} value
 * @returns {boolean}
 */
export function isString(value) {
    return typeof value === 'string' || value instanceof String;
}

/**
 * Returns a value indicating whether the value is a Function
 * @param {*} value
 * @returns {boolean}
 */
export function isFunction(value) {
    return typeof value === 'function';
}

/**
 * Returns a value indicating whether the value is an Object
 * @param {*} value
 * @returns {boolean}
 */
export function isObject(value) {
    return !isNullOrUndefined(value) && typeof value === 'object';
}

/**
 * Returns a value indicating whether the object is iterable
 * @param {*} obj
 * @returns {boolean}
 */
export function isIterable(obj) {
    return !isNullOrUndefined(obj) && typeof obj[Symbol.iterator] === 'function';
}

/**
 * Returns a value indicating whether the object is a non-string iterable
 * @param {*} obj
 * @returns {boolean}
 */
export function isCollection(obj) {
    return isIterable(obj) && !isString(obj);
}

/**
 * Returns a value indicating whether the value is null
 * @param {*} value
 * @returns {boolean}
 */
export function isNull(value) { 
    return value === null; 
}

/**
 * Returns a value indicating whether a string is null or made of whitespace.
 * @param {string} value string
 * @returns {boolean}
 */
export function isNullOrWhitespace(value) {
    return (!value || isString(value) && (value.length === 0 || /^\s*$/.test(value)));
}

/**
 * Returns a value indicating whether the value is undefined
 * @param {*} value
 * @returns {boolean}
 */
export function isUndefined(value) { 
    return typeof value === 'undefined'; 
}

/**
 * Returns a value indicating whether the value is null or undefined
 * @param {*} value
 * @returns {boolean}
 */
export function isNullOrUndefined(value) { 
    return isNull(value) || isUndefined(value); 
}