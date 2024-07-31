import {useSingleCleaningJob} from "../hooks/cleanings/useSingleCleaningJob";
import {useEffect, useState} from "react";
import {extractErrorMessages} from "./errors";
import validation from "./validation";


const formValidator = (initialForm) => {

    const [form, setForm] = useState({...initialForm});
    const [localErrors, setErrors] = useState({});
    const [hasSubmitted, setHasSubmitted] = useState(false);

    const cleaningErrorList = extractErrorMessages(serverErrors);
    const validateInput = (label, value) => {
        const isValid = validation?.[label] ? validation?.[label]?.(value) : true;
        setErrors((errors) => ({...errors, [label]: !isValid}));
    }
    const onInputChange = (label, value) => {
        validateInput(label, value);
        setForm((state) => ({...state, [label]: value}));
    }
    const onCleaningTypeChange = (cleaning_type) => {
        setForm((state) => ({ ...state, cleaning_type }));
    }
    const getFormErrors = () => {
        const formErrors = [];

        if (localErrors.form) {
            formErrors.push(localErrors.form);
        }
        if (hasSubmitted && cleaningErrorList.length) {
            return formErrors.concat(cleaningErrorList);
        }
        return formErrors;
    }
    return {
        form,
        setForm,
        localErrors,
        setErrors,
        isLoading,
        isUpdating,
        hasSubmitted,
        getFormErrors,
        setHasSubmitted,
        onInputChange,
        validateInput,
        onCleaningTypeChange,
        cleaningTypeOptions
    }
}