import React from 'react';
import {
    EuiPage,
    EuiPageBody,
    EuiPageContent_Deprecated,
    EuiPageContentBody_Deprecated,
    EuiPageHeader,
    EuiPageHeaderSection,
    EuiTitle,
} from '@elastic/eui';
import styled from "styled-components";

import { LoginForm } from "../../components";


const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`

const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem;
  
  & h1 {
    font-size: 3.5rem;
        font-weight: unset;
    color: #212121 !important;
  }
`

const StyledEuiPageHeaderSection = styled(EuiPageHeaderSection)`
  flex: 1;
  display: flex;
  justify-content: center;
`

export default function LoginPage() {
    return (
        <StyledEuiPage>
            <EuiPageBody component="section">
                <StyledEuiPageHeader>
                    <StyledEuiPageHeaderSection>
                        <EuiTitle size="l">
                            <h1>Login</h1>
                        </EuiTitle>
                    </StyledEuiPageHeaderSection>
                </StyledEuiPageHeader>
                <EuiPageContent_Deprecated verticalPosition="center" horizontalPosition="center">
                    <EuiPageContentBody_Deprecated>
                        <LoginForm />
                    </EuiPageContentBody_Deprecated>
                </EuiPageContent_Deprecated>
            </EuiPageBody>
        </StyledEuiPage>
    )
}