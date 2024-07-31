
export default {
    auth: {
        isLoading: false,
        error: false,
        user: {},
        users: {}
    },
    cleaning: {
        isLoading: false,
        isUpdating: false,
        error: null,
        data: {},
        currentCleaningJob: null,
        activeCleaningId: null,
    },
    offers: {
        isLoading: false,
        isUpdating: false,
        error: null,
        data: {}
    },
    feed: {
        isLoading: false,
        error: null,
        data: {},
        hasNext: {},
    },
    ui: {
        toastList: [],
    }
}