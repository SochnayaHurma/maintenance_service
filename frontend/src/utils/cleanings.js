export function userIsOwnerOfCleaningJob(cleaningJob, user) {
    if (cleaningJob?.owner?.id === user?.id) return true;
    if (cleaningJob?.owner === user?.id) return true;
}