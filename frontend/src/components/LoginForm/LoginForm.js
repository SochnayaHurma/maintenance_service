import React from 'react';
import {
    EuiForm,
    EuiFormRow,
    EuiButton,
    EuiSpacer,
    EuiFieldText,
    EuiFieldPassword,
} from '@elastic/eui';
import styled from 'styled-components';
import { Link } from "react-router-dom";
import { connect } from "react-redux";

import { Actions as authActions, FETCHING_USER_FROM_TOKEN_SUCCESS } from '../../redux/auth';
import { useLoginAndRegistrationForm} from "hooks/ui/useLoginAndRegistrationForm";

const LoginFormWrapper = styled.div`
  padding: 2rem;
`

const NeedAccountLink = styled.span`
  font-size: 0.8rem;
  color: #343741;
`

function LoginForm({ requestUserLogin }) {
    const {
        form,
        setForm,
        errors,
        setErrors,
        getFormErrors,
        handleInputChange,
        validateInput,
        setHasSubmitted
    } = useLoginAndRegistrationForm({ isLogin: true })
    const handleSubmit = async (e) => {
        e.preventDefault();

        Object.keys(form).forEach((label) => validateInput(label, form[label]));
        if (!Object.values(form).every((value) => Boolean(value))) {
            setErrors((errors) => ({...errors, form: "Все поля должны быть заполнены."}));
            return;
        }

        setHasSubmitted(true);
        const action = await requestUserLogin({email: form.email, password: form.password })
        if (action.type !== FETCHING_USER_FROM_TOKEN_SUCCESS) {
            setForm((form) => ({ ...form, password: ""}));
        }
    }

    return (
        <LoginFormWrapper>
            <EuiForm
                component="form"
                onSubmit={handleSubmit}
                isInvalid={Boolean(getFormErrors().length)}
                error={getFormErrors()}
            >
                <EuiFormRow
                    label="Email"
                    helpText="Enter the email associated with your account."
                    isInvalid={Boolean(errors.email)}
                    error={"Please enter a valid email."}
                >
                    <EuiFieldText
                        icon="email"
                        placeholder="user@gmail.com"
                        value={form.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        aria-label="Enter the email assciated with your account."
                        isInvalid={Boolean(errors.email)}
                    />
                </EuiFormRow>
                <EuiFormRow
                    label="Password"
                    helpText="Enter your password."
                    isInvalid={Boolean(errors.password)}
                    error={"Password must be at least 7 characters."}
                >
                    <EuiFieldPassword
                        placeholder="••••••••••••"
                        value={form.password}
                        onChange={(e) => handleInputChange("password", e.target.value)}
                        type="dual"
                        aria-label="Enter your password."
                        isInvalid={Boolean(errors.password)}
                    />
                </EuiFormRow>
                <EuiButton type="submit" fill>
                    Submit
                </EuiButton>
            </EuiForm>
            <EuiSpacer size="xl" />
            <NeedAccountLink>
                Need an account? Sing Up <Link to="/registration">here</Link>
            </NeedAccountLink>
        </LoginFormWrapper>
    )
}

const mapDispatchToProps = (dispatch) => ({
    requestUserLogin: ({email, password}) => dispatch(authActions.requestUserLogin({email, password}))
})

export default connect(null, mapDispatchToProps)(LoginForm)