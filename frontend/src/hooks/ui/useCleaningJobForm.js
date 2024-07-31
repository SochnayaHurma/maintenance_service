import React, {useEffect, useState} from 'react';
import {
    EuiText,
} from '@elastic/eui';

import {useSingleCleaningJob} from "hooks/cleanings/useSingleCleaningJob";
import { extractErrorMessages} from "utils/errors";
import validation from "utils/validation";

const cleaningTypeOptions = [
    {
        value: "dust_up",
        inputDisplay: "Очистка пыли",
        dropdownDisplay: (
            <React.Fragment>
                <strong>Очистка пыли</strong>
                <EuiText size="s" color="subdued">
                    <p>
                        Минимальная уборка. Протирка пыли с полок и каминов, наведение порядка в комнатах и уборка пыли с пола метлой.
                    </p>
                </EuiText>
            </React.Fragment>
        )
    },
    {
        value: "spot_clean",
        inputDisplay: "Очистка пятен",
        dropdownDisplay: (
            <React.Fragment>
                <strong>Очистка птяен</strong>
                <EuiText size="s" color="subdued">
                    <p>
                        Стандартная уборка. Пропылесосить все помещения, продезинфицировать поверхности. (Ванные комнаты и туалеты за дополнительную плату)
                    </p>
                </EuiText>
            </React.Fragment>
        )
    },
    {
        value: "full_clean",
        inputDisplay: "Полная уборка",
        dropdownDisplay: (
            <React.Fragment>
                <strong>Полная уборка</strong>
                <EuiText size="s" color="subdued">
                    <p>
                        Максимальная уборка. Протирка полов и чистка труднодоступных поверхностей. Мойка любой посуды.
                    </p>
                </EuiText>
            </React.Fragment>
        )
    }
]

export const useCleaningJobForm = (cleaningId) => {

    const { cleaningJob, error: serverErrors, isLoading, isUpdating,  } = useSingleCleaningJob(cleaningId);
    const [form, setForm] = useState({
        name: cleaningJob?.name || "",
        description: cleaningJob?.description || "",
        price: cleaningJob?.price || "",
        cleaning_type: cleaningJob?.cleaning_type || cleaningTypeOptions[0].value
    });
    const [localErrors, setErrors] = useState({});
    const [hasSubmitted, setHasSubmitted] = useState(false);

    const cleaningErrorList = extractErrorMessages(serverErrors);
    useEffect(() => {
        if (cleaningJob) {
            setForm((form) => ({ ...cleaningJob }))
        }
    }, [cleaningJob]);
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