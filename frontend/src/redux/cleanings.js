import initialState from './initialState';
import apiClient from "../services/apiClient";
import {REQUEST_LOG_USER_OUT, RECEIVED_ALL_CLEANING_USERS_SUCCESS} from "./auth";
import {
    FETCH_ALL_OFFERS_FOR_CLEANING_JOB,
    FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS,
    FETCH_USER_OFFER_FOR_CLEANING_JOB_SUCCESS
} from "./offers";
import {Actions as uiActions} from './ui';
import ApiClient from "../services/apiClient";

export const CREATE_CLEANING_JOB = "@@cleanings/CREATE_CLEANING_JOB";
export const CREATE_CLEANING_SUCCESS = "@@cleanings/CREATE_CLEANING_JOB_SUCCESS"
export const CREATE_CLEANING_FAILURE = "@@cleanings/CREATE_CLEANING_JOB_FAILURE"
export const FETCH_CLEANING_BY_ID = "@@cleanings/FETCH_CLEANING_JOB_BY_ID"
export const FETCH_CLEANING_BY_ID_SUCCESS = "@@cleanings/FETCH_CLEANING_JOB_BY_ID_SUCCESS"
export const FETCH_CLEANING_BY_ID_FAILURE = "@@cleanings/FETCH_CLEANING_JOB_BY_ID_FAILURE"
export const CLEAR_CURRENT_CLEANING_JOB = "@@cleanings/CLEAR_CURRENT_CLEANING_JOB";
export const UPDATE_CLEANING_JOB = "@@cleanings/UPDATE_CLEANING_JOB";
export const UPDATE_CLEANING_JOB_SUCCESS = "@@cleanings/UPDATE_CLEANING_JOB_SUCCESS";
export const UPDATE_CLEANING_JOB_FAILURE = "@@cleanings/UPDATE_CLEANING_JOB_FAILURE";
export const DELETE_CLEANING_JOB = "@@cleaning/DELETE_CLEANING_JOB";
export const DELETE_CLEANING_JOB_SUCCESS = "@@cleaning/DELETE_CLEANING_JOB_SUCCESS";
export const DELETE_CLEANING_JOB_FAILURE = "@@cleaning/DELETE_CLEANING_JOB_FAILURE";
export const FETCH_ALL_USER_OWNED_CLEANING_JOB = "@@cleanings/FETCH_ALL_USER_OWNED_CLEANING_JOB";
export const FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS = "@@cleanings/FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS";
export const FETCH_ALL_USER_OWNED_CLEANING_JOB_FAILURE = "@@cleanings/FETCH_ALL_USER_OWNED_CLEANING_JOB_FAILURE";
export const FETCH_ALL_CLEANING_RECEIVED_DATA_SUCCESS = "@@cleanings/FETCH_ALL_CLEANING_RECEIVED_DATA_SUCCESS";

export default function cleaningReducer(state = initialState.cleaning, action = {}) {
    switch (action.type) {
        case CREATE_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case CREATE_CLEANING_SUCCESS:
            return {
                ...state,
                isLoading: false,
                error: null,
                data: {
                    ...state.data,
                    [action.data.id]: action.data,
                },
            }
        case CREATE_CLEANING_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }

        case FETCH_CLEANING_BY_ID:
            return {
                ...state,
                isLoading: true,
            }
        case FETCH_CLEANING_BY_ID_SUCCESS:
            return {
                ...state,
                isLoading: false,
                error: null,
                currentCleaningJob: action.data.cleaning,
                activeCleaningId: action.data.cleaning.id
            }
        case FETCH_CLEANING_BY_ID_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error,
                currentCleaningJob: {}
            }
        case CLEAR_CURRENT_CLEANING_JOB:
            return {
                ...state,
                currentCleaningJob: null
            }
        case UPDATE_CLEANING_JOB:
            return {
                ...state,
                isUpdating: true
            }
        case UPDATE_CLEANING_JOB_SUCCESS:
            return {
                ...state,
                isUpdating: false,
                error: null,
                data: {
                    ...state.data,
                    [action.data.id]: action.data
                }
            }
        case UPDATE_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isUpdating: false,
                error: action.error
            }
        case DELETE_CLEANING_JOB:
            return {
                ...state,
                isLoading: true,
            }
        case DELETE_CLEANING_JOB_SUCCESS:
            const newData = Object.keys(state.data)
                .reduce((ac, el) => {
                    if (el !== action.data.toString()) {
                        ac[el] = state.data[el]
                    }
                    return ac
                }, {})

            return {
                ...state,
                isLoading: false,
                data: {...newData}
            }

        case DELETE_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }

        case FETCH_ALL_USER_OWNED_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS:
            return {
                ...state,
                isLoading: false,
                error: null,
                data: {...state.data, ...action.data}
            }
        case FETCH_ALL_USER_OWNED_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case REQUEST_LOG_USER_OUT:
            return initialState.cleaning;
        default:
            return state;
    }
}

export const Actions = {};

Actions.createCleaningJob = ({newCleaning}) => {
    return (dispatch) => dispatch(
        apiClient({
            url: '/cleanings/',
            method: 'POST',
            types: {
                REQUEST: CREATE_CLEANING_JOB,
                SUCCESS: CREATE_CLEANING_SUCCESS,
                FAILURE: CREATE_CLEANING_FAILURE
            },
            options: {
                data: {new_cleaning: {...newCleaning}},
                params: {}
            },
            onSuccess: (response) => {
                dispatch({type: CREATE_CLEANING_SUCCESS, data: response.data});
                return {success: true, data: response.data}
            }
        }))
}

Actions.fetchCleaningJobById = ({cleaningId}) => {
    return (dispatch) => dispatch(apiClient({
        url: `/cleanings/${cleaningId}`,
        method: 'GET',
        types: {
            REQUEST: FETCH_CLEANING_BY_ID,
            SUCCESS: FETCH_CLEANING_BY_ID_SUCCESS,
            FAILURE: FETCH_CLEANING_BY_ID_FAILURE
        },
        options: {
            data: {},
            params: {}
        },
        onSuccess: (response) => {
            const cleaning = {
                [response.data?.cleaning?.id]: {...response.data?.cleaning, owner: response.data?.cleaning?.owner?.id}
            }
            dispatch({
                type: FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS,
                success: true,
                status: response.status,
                data: cleaning
            })
            dispatch({
                type: RECEIVED_ALL_CLEANING_USERS_SUCCESS,
                success: true,
                status: response.status,
                data: {[response.data?.cleaning?.owner.id]: response.data?.cleaning?.owner}
            })
        }
    }))
}

Actions.fetchAllUserOwnedJobs = () => {
    return (dispatch) => dispatch(apiClient({
        url: `/cleanings/`,
        method: 'GET',
        types: {
            REQUEST: FETCH_ALL_OFFERS_FOR_CLEANING_JOB,
            SUCCESS: FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS,
            FAILURE: FETCH_ALL_USER_OWNED_CLEANING_JOB_FAILURE
        },
        options: {data: {}, params: {}},
        onSuccess: (response) => {
            const users = {}
            const cleanings = {}
            const offers = {}
            response.data.forEach((el) => {
                cleanings[el.cleaning.id] = {...el.cleaning, owner: el.cleaning.owner.id}
                users[el?.cleaning?.owner?.id] = el?.cleaning?.owner
                if (el?.offers?.length !== 0) {
                    offers[el?.cleaning?.id] = el?.offers?.reduce((acc, el) => {
                        users[el?.executor?.id] = el?.executor;
                        return {...acc, [el?.executor?.id]: {...el, executor: el?.executor?.id}}
                    }, {})
                }
            })
            dispatch({
                type: FETCH_ALL_USER_OWNED_CLEANING_JOB_SUCCESS,
                success: true,
                status: response.status,
                data: cleanings
            })
            dispatch({
                type: RECEIVED_ALL_CLEANING_USERS_SUCCESS,
                success: true,
                status: response.status,
                data: users
            })
            dispatch({
                type: FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS,
                success: true,
                data: offers
            })
        }
    }))
}

Actions.updateCleaningJob = ({cleaningId, cleaningUpdate}) => {
    return (dispatch) => {
        return dispatch(apiClient({
            url: `/cleanings/${cleaningId}/`,
            method: 'PUT',
            types: {
                REQUEST: UPDATE_CLEANING_JOB,
                SUCCESS: UPDATE_CLEANING_JOB_SUCCESS,
                FAILURE: UPDATE_CLEANING_JOB_FAILURE
            },
            options: {
                data: {cleaning_update: {...cleaningUpdate}},
                params: {}
            },
            onSuccess: (response) => {
                dispatch({type: UPDATE_CLEANING_JOB_SUCCESS, data: response.data})
                dispatch(
                    uiActions.addToast({
                        id: 'update-cleaning-success',
                        title: "Обновлено",
                        color: "success",
                        iconType: "checkInCircleFilled",
                        toastLifeTimeMs: 15000,
                        text: "Ваша услуга удачно обновлена"
                    })
                )
                return {
                    type: UPDATE_CLEANING_JOB_SUCCESS,
                    success: true,
                    status: response.status,
                    data: response.data
                }
            }
        }))
    }
}

Actions.deleteCleaningJob = ({cleaningId}) => {
    return (dispatch) => dispatch(
        ApiClient({
            url: `/cleanings/${cleaningId}/`,
            method: 'DELETE',
            types: {
                REQUEST: DELETE_CLEANING_JOB,
                SUCCESS: DELETE_CLEANING_JOB_SUCCESS,
                FAILURE: DELETE_CLEANING_JOB_FAILURE
            },
            options: {
                data: {},
                params: {}
            },
            onSuccess: (response) => {
                dispatch({type: DELETE_CLEANING_JOB_SUCCESS, data: cleaningId});
            }
    }))
}

Actions.clearCurrentCleaningJob = () => ({type: CLEAR_CURRENT_CLEANING_JOB});