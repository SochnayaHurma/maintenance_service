import React, {useState} from 'react';
import { connect } from 'react-redux';
import {useNavigate} from "react-router-dom";

import { Actions as cleaningActions } from 'redux/cleanings';
import {useCleaningJobForm} from "hooks/ui/useCleaningJobForm";
import CleaningJobsCreateForm from "./CleaninbJobsCreateForm"


function CleaningJobsCreatePage({ createCleaning }) {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const {
        form,
        localErrors,
        getFormErrors,
        setErrors,
        setHasSubmitted,
        validateInput,
        onInputChange,
        cleaningTypeOptions,
        onCleaningTypeChange,
    } = useCleaningJobForm();

    const handleSubmit = async (e) => {
        e.preventDefault();

        Object.keys(form).forEach((label) => validateInput(label, form[label]));

        if (!Object.values(form).every((value) => Boolean(value))) {
            setErrors((errors) => ({ ...errors, form: "Все поля должны быть заполнены." }));
            return;
        }
        setHasSubmitted(true);

        const response = await createCleaning({ newCleaning: {...form}});
        if (response.success) {
            const cleaningId = response.data?.id;
            navigate(`/cleaning-jobs/${cleaningId}`);
        }
    }
    return (
        <CleaningJobsCreateForm
            form={form}
            handleSubmit={handleSubmit}
            getFormErrors={getFormErrors}
            localErrors={localErrors}
            onInputChange={onInputChange}
            onCleaningTypeChange={onCleaningTypeChange}
            isLoading={isLoading}
            cleaningTypeOptions={cleaningTypeOptions}
        />
    )
}


const mapDispatchToProps = {
    createCleaning: cleaningActions.createCleaningJob
}

export default connect(null, mapDispatchToProps)(CleaningJobsCreatePage);