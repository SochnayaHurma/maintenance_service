import axios from "axios";
import { formatURL } from "../utils/urls";


const getClient = (token = null) => {
    const defaultOptions = {
        headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Bearer ${token}` : ""
        }
    }

    return {
        get: (url, data, options = {}) => axios.get(url, {...defaultOptions, ...options}),
        post: (url, data, options = {}) => axios.post(url, data, {...defaultOptions, ...options}),
        put: (url, data, options = {}) => axios.put(url, data, {...defaultOptions, ...options}),
        delete: (url, data, options = {}) => axios.delete(url, {...defaultOptions, ...options})
    }
}

/**
 *
 * @param {String} url
 * @param {String} method
 * @param {Object} types
 * @param {Object} options
 * @param {Function} onSuccess
 * @param {Function} onFailure
 */
const apiClient = ({
    url,
    method,
    types: { REQUEST, SUCCESS, FAILURE },
    options: { data, params },
    onSuccess = (res) => ({type: res.type, success: true, status: res.status, data: res.data}),
    onFailure = (res) => ({type: res.type, success: false, status: res.status, error: res.error}),
                   }) => {
    return async (dispatch) => {
        const token = localStorage.getItem("access_token");
        const client = getClient(token);
        dispatch({ type: REQUEST });
        const urlPath = formatURL(url, params);

        try {
            const response = await client[method.toLowerCase()](urlPath, data);

            // dispatch({ type: SUCCESS, data: response.data });
            return onSuccess({ type: SUCCESS, ...response })
        } catch (error) {
            console.log(error);
            dispatch({
                type: FAILURE,
                error: error?.response?.data ? error.response.data : error
            })

            return onFailure({ type: FAILURE, status: error.status, error: error.response })
        }

    }
}

export default apiClient;