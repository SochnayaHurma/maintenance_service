import initialState from './initialState';
import {REQUEST_LOG_USER_OUT} from './auth'
import moment from 'moment';
import apiClient from "../services/apiClient";


export const FETCH_CLEANING_FEED_ITEMS = "@@feed/FETCH_CLEANING_FEED_ITEMS";
export const FETCH_CLEANING_FEED_ITEMS_SUCCESS = "@@feed/FETCH_CLEANING_FEED_ITEMS_SUCCESS";
export const FETCH_CLEANING_FEED_ITEMS_FAILURE = "@@feed/FETCH_CLEANING_FEED_ITEMS_FAILURE";
export const SET_HAS_NEXT_FOR_NEED = "@@feed/SET_HAS_NEXT_FOR_FEED";

let q = true

export default function feedReducer(state = initialState.feed, action = {}) {
    switch (action.type) {
        case FETCH_CLEANING_FEED_ITEMS:
            return {
                ...state,
                isLoading: true
            }
        case FETCH_CLEANING_FEED_ITEMS_SUCCESS:
            return {
                ...state,
                isLoading: false,
                error: null,
                data: {
                    ...state.data,
                    cleaning: [
                        ...(state.data.cleaning || []),
                        ...action.data,
                    ]
                }
            }
        case FETCH_CLEANING_FEED_ITEMS_FAILURE:
            return {
                ...state,
                isLoading: false,
                error: action.error
            }
        case SET_HAS_NEXT_FOR_NEED:
            return {
                ...state,
                hasNext: {
                    ...state.hasNext,
                    [action.feed]: action.next
                }
            }
        case REQUEST_LOG_USER_OUT:
            return initialState.feed;
        default:
            return state;
    }
}

export const Actions = {};

Actions.fetchCleaningFeedItem = (starting_date = new Date(), page_size_chunk = 20) => {
    return (dispatch) => {
        return dispatch(
            apiClient({
                url: `/feed/cleanings/`,
                method: `GET`,
                types: {
                    REQUEST: FETCH_CLEANING_FEED_ITEMS,
                    SUCCESS: FETCH_CLEANING_FEED_ITEMS_SUCCESS,
                    FAILURE: FETCH_CLEANING_FEED_ITEMS_FAILURE,
                },
                options: {
                    data: {},
                    params: {
                        starting_date: moment(starting_date).format(),
                        page_size_chunk,
                    },
                },
                onSuccess: (response) => {
                    dispatch({
                        type: SET_HAS_NEXT_FOR_NEED,
                        feed: "cleaning",
                        hasNext: Boolean(response?.data?.length === page_size_chunk)
                    });
                    return { success: true, status: response.status, data: response.data }
                }
            })
        )
    }
}