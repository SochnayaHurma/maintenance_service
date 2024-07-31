import React from 'react';
import {
    EuiPage,
    EuiPageHeader,
    EuiPageBody,
    EuiTitle,
    EuiPageContent_Deprecated, EuiPageHeaderSection, EuiPageContentBody_Deprecated,
} from '@elastic/eui';
import styled from 'styled-components';
import {RegistrationForm} from "../../components";


const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`

const StyledEuiPageHeader = styled(EuiPageHeader)`
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

export default function RegistrationPage() {
    return (
        <StyledEuiPage>
            <EuiPageBody component="section">
                <StyledEuiPageHeader>
                    <StyledEuiPageHeaderSection>
                        <EuiTitle size="lx">
                            <h1>Sign Up</h1>
                        </EuiTitle>
                    </StyledEuiPageHeaderSection>
                </StyledEuiPageHeader>
                <EuiPageContent_Deprecated verticalPosition="center" horizontalPosition="center">
                    <EuiPageContentBody_Deprecated>
                        <RegistrationForm/>
                    </EuiPageContentBody_Deprecated>
                </EuiPageContent_Deprecated>
            </EuiPageBody>
        </StyledEuiPage>
    )
}