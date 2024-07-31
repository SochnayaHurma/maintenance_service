import { shallowEqual, useDispatch, useSelector } from "react-redux";
import {useCallback, useEffect, useState} from "react";

import { Actions as feedActions } from 'redux/feed';


export default function useCleaningFeed() {
    const dispatch = useDispatch();
    const isLoading = useSelector((state) => state.feed.isLoading);
    const error = useSelector((state) => state.feed.error, shallowEqual);
    const feedItems = useSelector((state) => state.feed.data?.cleaning, shallowEqual);
    const hasNext = useSelector((state) => state.feed.hasNext.cleaning);

    const fetchFeedItems = useCallback((starting_date, page_chunk_size) => {
        return dispatch(feedActions.fetchCleaningFeedItem(starting_date, page_chunk_size));
    }, [dispatch]);
    useEffect(() => {
        fetchFeedItems();
    }, []);
    return { isLoading, error, feedItems, hasNext, fetchFeedItems};
}