/**
 *
 * @param {String} base
 * @param {Object} params
 */
export const formatURLWithQueryParams = (base, params) => {
    if (!params || Object.keys(params)?.length === 0) return base;

    const query = Object.entries(params)
        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
        .join("&");
    return `${base}?${query}`
}

/**
 *
 * @param {String} path
 */
export const formatAPIPath = (path) => {
    let adjustedPath = path;
    if (adjustedPath.charAt(0) !== "/") {
        adjustedPath = "/" + adjustedPath;
    }
    if (adjustedPath.charAt(adjustedPath.length - 1) !== "/") {
        adjustedPath = adjustedPath + "/";
    }
    return adjustedPath
}

/**
 *
 * @param {String} url
 * @param {Object} params
 */
export const formatURL = (url, params) => {
    const endpointPath = formatAPIPath(url);
    const baseUrl = process.env.NODE_ENV === "production"
                        ? process.env.REMOVE_SERVER_URL
                        : "http://localhost:8000/api";
    const fullURL = `${baseUrl}${endpointPath}`;
    return formatURLWithQueryParams(fullURL, params);
}