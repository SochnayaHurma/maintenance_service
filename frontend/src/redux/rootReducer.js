import { combineReducers } from "redux";

import authReducer from "./auth";
import cleaningReducer from "./cleanings";
import offersReducer from "./offers";
import feedReducer from "./feed";
import uiReducer from "./ui";

const rootReducer = combineReducers({
    auth: authReducer,
    cleaning: cleaningReducer,
    offers: offersReducer,
    feed: feedReducer,
    ui: uiReducer,
})

export default rootReducer;