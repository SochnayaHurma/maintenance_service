import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { extractErrorMessages } from "utils/errors";
import validation from "utils/validation";

export const useLoginAndRegistrationForm = ({ isLogin = false }) => {
    const { user, error: authError, isLoading, isAuthenticated } = useAuthenticatedUser();
    const [ form, setForm ] = useState({
        username: "",
        email: "",
        password: "",
        passwordConfirm: "",
    })
    const [agreedToTerms, setAgreedToTerms] = useState(false);
    const [errors, setErrors] = useState({});
    const [hasSubmitted, setHasSubmitted] = useState(false);

    const authErrorList = extractErrorMessages(authError);
    const navigate = useNavigate();

    const validateInput = (label, value) => {
        const isValid = validation?.[label] ? (
            validation?.[label]?.(value)
        ) : true;
        setErrors((errors) => ({...errors, [label]: !isValid}))
    }
    const handleInputChange = (label, value) => {
        validateInput(label, value);
        setForm((form) => ({...form, [label]: value}));
    }
    const handlePasswordConfirmChange = (value) => {
        setErrors((errors) => ({
            ...errors,
            passwordConfirm: form.password !== value ? (
                `Пароли не совпадают.`
            ) : null
        }));
        setForm((form) => ({...form, passwordConfirm: value}));
    }
    const getFormErrors = () => {
        const formErrors = [];

        if (errors.form) {
            formErrors.push(errors.form);
        }
        if (hasSubmitted && authErrorList.length) {
            const additionalErrors = isLogin
                                    ? [`Неверные данные. Попоробуйте снова.`]
                                    : authErrorList;
            return formErrors.concat(additionalErrors);
        }
        return formErrors;
    }

    useEffect(() => {
        if (user?.email && isAuthenticated) {
            navigate("/profile");
        }
    }, [user, navigate, isAuthenticated])
    return {
        form: isLogin ? (
            { email: form.email, password: form.password }
        ) : form,
        setForm,
        errors,
        setErrors,
        isLoading,
        getFormErrors,
        hasSubmitted,
        setHasSubmitted,
        handleInputChange,
        validateInput,
        agreedToTerms,
        setAgreedToTerms,
        handlePasswordConfirmChange
    }
}