import React from 'react';
import {connect} from 'react-redux';
import styled from 'styled-components';

import {Actions as cleaningActions} from '../../redux/cleanings';
import { useCleaningJobForm } from "hooks/ui/useCleaningJobForm";
import {useNavigate} from "react-router-dom";
import CleaningJobsCreateForm from "../CleaningJobsCreateForm/CleaninbJobsCreateForm";


const Wrapper = styled.div`
  padding: 1rem 2rem;
`


function CleaningJobEditForm({cleaningId, updateCleaning}) {
    const navigate = useNavigate();
    const {
        isUpdating,
        form,
        localErrors,
        setErrors,
        getFormErrors,
        validateInput,
        onInputChange,
        setHasSubmitted,
        cleaningTypeOptions,
        onCleaningTypeChange,
    } = useCleaningJobForm(cleaningId)

    const handleSubmit = async (e) => {
        e.preventDefault();

        Object.keys(form).forEach((label) => validateInput(label, form[label]));

        if (!Object.values(form).every((value) => Boolean(value))) {
            setErrors((errors) => ({...errors, form: "Все поля должны быть заполнены."}));
            return;
        }
        setHasSubmitted(true);
        const response = await updateCleaning({cleaningId, cleaningUpdate: {...form}});
        if (response?.success) {
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
            isLoading={isUpdating}
            cleaningTypeOptions={cleaningTypeOptions}
        />
    )
}


const mapDispatchToProps = {
    updateCleaning: cleaningActions.updateCleaningJob
}
export default connect(null, mapDispatchToProps)(CleaningJobEditForm);