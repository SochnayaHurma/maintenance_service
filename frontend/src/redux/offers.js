import initialState from "./initialState";
import apiClient from "../services/apiClient";
import { REQUEST_LOG_USER_OUT} from "./auth";
import {UPDATE_CLEANING_JOB, UPDATE_CLEANING_JOB_FAILURE, UPDATE_CLEANING_JOB_SUCCESS} from "./cleanings";

export const CREATE_OFFER_FOR_CLEANING_JOB = "@@offers/CREATE_OFFER_FOR_CLEANING_JOB";
export const CREATE_OFFER_FOR_CLEANING_JOB_SUCCESS = "@@offers/CREATE_OFFER_FOR_CLEANING_JOB_SUCCESS";
export const CREATE_OFFER_FOR_CLEANING_JOB_FAILURE = "@@offers/CREATE_OFFER_FOR_CLEANING_JOB_FAILURE";
export const ACCEPT_OFFER_CLEANING_JOB = "@@offers/ACCEPT_OFFER_CLEANING_JOB";
export const ACCEPT_OFFER_CLEANING_JOB_SUCCESS = "@@offers/ACCEPT_OFFER_CLEANING_JOB_SUCCESS";
export const ACCEPT_OFFER_CLEANING_JOB_FAILURE = "@@offers/ACCEPT_OFFER_CLEANING_JOB_FAILURE";
export const CANCEL_OFFER_CLEANING_JOB = "@@offers/CANCEL_OFFER_CLEANING_JOB";
export const CANCEL_OFFER_CLEANING_JOB_SUCCESS = "@@offers/CANCEL_OFFER_CLEANING_JOB_SUCCESS";
export const CANCEL_OFFER_CLEANING_JOB_FAILURE = "@@offers/CANCEL_OFFER_CLEANING_JOB_FAILURE";

export const FETCH_USER_OFFER_FOR_CLEANING_JOB = "@@offers/FETCH_USER_OFFER_FOR_CLEANING_JOB";
export const FETCH_USER_OFFER_FOR_CLEANING_JOB_SUCCESS = "@@offers/FETCH_USER_OFFER_FOR_CLEANING_JOB_SUCCESS";
export const FETCH_USER_OFFER_FOR_CLEANING_JOB_FAILURE = "@@offers/FETCH_USER_OFFER_FOR_CLEANING_JOB_FAILURE";
export const FETCH_ALL_OFFERS_FOR_CLEANING_JOB = "@@offers/FETCH_ALL_OFFERS_FOR_CLEANING_JOB";
export const FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS = "@@offers/FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS";
export const FETCH_ALL_OFFERS_FOR_CLEANING_JOB_FAILURE = "@@offers/FETCH_ALL_OFFERS_FOR_CLEANING_JOB_FAILURE";
function updateStateWithOfferForCleaning(state, offers) {
    const cleaningId = offers?.[0]?.cleaning_id;
    const offersIndexedUserId = offers?.reduce((acc, offer) => {
        acc[offer.user_id] = offer;
        return acc;
    }, {})
    const test =  {
        ...state,
        isLoading: false,
        error: null,
        data: {
            ...state.data,
            ...(cleaningId ? {
                [cleaningId]: {
                    ...(state.data[cleaningId] || {}),
                    ...offersIndexedUserId
                }
            } : {})
        }
    }
    return test
}


export default function offersReducer(state = initialState.offers, action = {}) {
    switch (action.type) {
        case CREATE_OFFER_FOR_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case CREATE_OFFER_FOR_CLEANING_JOB_SUCCESS:
            return updateStateWithOfferForCleaning(state, [action.data]);
        case CREATE_OFFER_FOR_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case UPDATE_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case UPDATE_CLEANING_JOB_SUCCESS:
            return {
                ...state,
                isLoading: false
            }
        case UPDATE_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case CANCEL_OFFER_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case CANCEL_OFFER_CLEANING_JOB_SUCCESS:
            return {
                ...state,
                isLoading: false
            }
        case CANCEL_OFFER_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case FETCH_USER_OFFER_FOR_CLEANING_JOB:
            return {
                ...state,
                isLoading: true,

            }
        case FETCH_USER_OFFER_FOR_CLEANING_JOB_SUCCESS:
            return updateStateWithOfferForCleaning(state, [action.data]);
        case FETCH_USER_OFFER_FOR_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                // error: action.error
            }
        case FETCH_ALL_OFFERS_FOR_CLEANING_JOB:
            return {
                ...state,
                isLoading: true
            }
        case FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS:
            return {
                ...state,
                isLoading: false,
                data: {
                    ...state.data,
                    ...action.data
                }
            }
        case FETCH_ALL_OFFERS_FOR_CLEANING_JOB_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case REQUEST_LOG_USER_OUT:
            return initialState.offers;
        default:
            return state;
    }
}

export const Actions = {};

Actions.createOfferForCleaning = ({ cleaningId }) => {
    return (dispatch) => dispatch(
        apiClient({
            url: `/cleanings/${cleaningId}/offer/`,
            method: 'POST',
            types: {
                REQUEST: CREATE_OFFER_FOR_CLEANING_JOB,
                SUCCESS: CREATE_OFFER_FOR_CLEANING_JOB_SUCCESS,
                FAILURE: CREATE_OFFER_FOR_CLEANING_JOB_FAILURE
            },
            options: {
                data: {},
                params: {}
            },
            onSuccess: (response) => {
                dispatch({ type: CREATE_OFFER_FOR_CLEANING_JOB_SUCCESS, data: response.data });
            }
        })
    )
}

Actions.acceptUserOfferForCleaningJob = ({ cleaningId, username}) => {
    return (dispatch) => dispatch(
        apiClient({
            url: `/cleanings/${cleaningId}/offer/${username}/`,
            method: `PUT`,
            types: {
                REQUEST: ACCEPT_OFFER_CLEANING_JOB,
                SUCCESS: ACCEPT_OFFER_CLEANING_JOB_SUCCESS,
                FAILURE: ACCEPT_OFFER_CLEANING_JOB_FAILURE,
            },
            options: {
                data: {},
                params: {},
            },
            onSuccess: (response) => {
                dispatch({type: ACCEPT_OFFER_CLEANING_JOB_SUCCESS, data: response.data});
            }
        })
    )
}
Actions.cancelUserOfferForCleaningJob = ({ cleaningId }) => {
    return (dispatch) => dispatch(
        apiClient({
            url: `/cleanings/${cleaningId}/offer/`,
            method: `PUT`,
            types: {
                REQUEST: CANCEL_OFFER_CLEANING_JOB,
                SUCCESS: CANCEL_OFFER_CLEANING_JOB_SUCCESS,
                FAILURE: CANCEL_OFFER_CLEANING_JOB_FAILURE,
            },
            options: {
                data: {},
                params: {},
            },
            onSuccess: (response) => {
                dispatch({type: CANCEL_OFFER_CLEANING_JOB_SUCCESS, data: response.data});
            }
        })
    )
}

Actions.fetchUserOfferForCleaningJob = ({ cleaning_id, username }) => {
    return apiClient({
        url: `/cleanings/${cleaning_id}/offer/${username}/`,
        method: 'GET',
        types: {
            REQUEST: FETCH_USER_OFFER_FOR_CLEANING_JOB,
            SUCCESS: FETCH_USER_OFFER_FOR_CLEANING_JOB_SUCCESS,
            FAILURE: FETCH_USER_OFFER_FOR_CLEANING_JOB_FAILURE
        },
        options: {
            data: {},
            params: {}
        }
    })
}

Actions.fetchAllOffersForCleaningJob = ({ cleaning_id }) => {
    return apiClient({
        url: `/cleanings/${cleaning_id}/offer/`,
        method: `GET`,
        types: {
            REQUEST: FETCH_ALL_OFFERS_FOR_CLEANING_JOB,
            SUCCESS: FETCH_ALL_OFFERS_FOR_CLEANING_JOB_SUCCESS,
            FAILURE: FETCH_ALL_OFFERS_FOR_CLEANING_JOB_FAILURE
        },
        options: {data: {}, params: {}}
    })
}