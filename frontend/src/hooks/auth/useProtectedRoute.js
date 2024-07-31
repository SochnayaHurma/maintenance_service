import {useEffect} from "react";
import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { useToasts } from "hooks/ui/useToasts";


export const useProtectedRoute = (
    redirectTitle = `Доступ запрещен`,
    redirectMessage = `Только вошедшие пользователи имеют доступ к данной странице. Войдите на сайт или зарегистрируйте новый аккаунт чтобы получить доступ.`
) => {
    const { userLoaded, isAuthenticated } = useAuthenticatedUser();
    const { addToast } = useToasts();
    useEffect(() => {
        if (userLoaded && !isAuthenticated) {
            addToast({
                id: `auth-toast-redirect`,
                title: redirectTitle,
                color: "warning",
                iconType: "alert",
                toastLifeTimeMs: 15000,
                text: redirectMessage
            })
        }
    }, [userLoaded, isAuthenticated, redirectTitle, redirectMessage]);
    return { userLoaded, isAuthenticated };
}