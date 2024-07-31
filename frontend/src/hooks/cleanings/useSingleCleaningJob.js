import { useEffect } from "react";
import { useDispatch, useSelector, shallowEqual } from "react-redux";

import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { userIsOwnerOfCleaningJob } from 'utils/cleanings';
import { Actions as cleaningActions } from 'redux/cleanings';


export const useSingleCleaningJob = ( cleaningId ) => {
    const dispatch = useDispatch();

    const { user } = useAuthenticatedUser();
    const cleaningJob = useSelector((state) => state.cleaning.data[cleaningId], shallowEqual);
    const activeCleaningId = useSelector((state) => state.cleaning.activeCleaningId);
    const isLoading = useSelector((state) => state.cleaning.isLoading);
    const isUpdating = useSelector((state) => state.cleaning.isUpdating);
    const error = useSelector((state) => state.cleaning.error, shallowEqual);
    const userIsOwner = userIsOwnerOfCleaningJob(cleaningJob, user);
    useEffect(() => {
        if (cleaningId && !cleaningJob) {
            dispatch(cleaningActions.fetchCleaningJobById({ cleaningId }));
        }

        return () => {
            dispatch(cleaningActions.clearCurrentCleaningJob());
        }
    }, [dispatch, cleaningId, cleaningJob]);

    return {
        error,
        isLoading,
        isUpdating,
        cleaningJob,
        userIsOwner,
        activeCleaningId
    }
}