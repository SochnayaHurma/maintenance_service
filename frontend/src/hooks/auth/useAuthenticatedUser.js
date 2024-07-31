import { useDispatch, useSelector, shallowEqual } from "react-redux";
import { Actions as authActions } from "redux/auth";


export const useAuthenticatedUser = () => {
    const dispatch = useDispatch();
    const user = useSelector((state) => state.auth.user, shallowEqual)
    const isLoading = useSelector((state) => state.auth.isLoading);
    const isUpdating = useSelector((state) => state.auth.isUpdating);
    const error = useSelector((state) => state.auth.error);
    const userLoaded = useSelector((state) => state.auth.userLoaded);
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

    const logUserOut = () => dispatch(authActions.logUserOut());
    return { user, isLoading, isUpdating, error, userLoaded, isAuthenticated, logUserOut }
}
