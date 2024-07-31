import React from 'react';
import {
    EuiPage,
    EuiPageBody,
    EuiPageHeader,
    EuiPageContent_Deprecated,
    EuiPageContentBody_Deprecated,
    EuiAccordion,
    EuiSpacer,
    EuiIcon,
} from '@elastic/eui';
import {connect} from 'react-redux';
import styled from 'styled-components';

import {CleaningJobsCreatePage, CleaningActivityFeed} from "../../components";

const StyledEuiPage = styled(EuiPage)`
  flex: 1;

  & .create-new-job-button {
    display: flex;
    justify-content: center;
    background-color: #f5f3f3;

    & > span {
      font-size: 1.2rem;
      font-weight: bold;
      text-decoration: none;
    }

    &:hover {
      & > span {
        color: dodgerblue;
      }
    }
  }
`

const StyledEuiHeader = styled(EuiPageHeader)`
  margin: 2rem;
  & h1 {
    font-size: 3.5rem;
    color: #212121 !important;
  }
`
const StyledTitle = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
`

function CleaningJobsHome({user}) {
    const newJobButtonContent = (
        <>
            <EuiIcon type="broom" size="l" />
            Post A New Cleaning Job
        </>
    )
    return (
        <StyledEuiPage>
            <EuiPageBody component="section">
                <StyledEuiHeader>
                    <StyledTitle>
                        <h1>Cleaning Jobs</h1>
                    </StyledTitle>
                </StyledEuiHeader>
                <EuiPageContent_Deprecated horizontalPosition="center">
                    <EuiPageContentBody_Deprecated>
                        <EuiAccordion
                            id="create-new-job-button"
                            buttonClassName="create-new-job-button"
                            buttonContent={newJobButtonContent}
                            arrowDisplay="none"
                            paddingSize="m"

                        >
                            <CleaningJobsCreatePage />
                        </EuiAccordion>
                    </EuiPageContentBody_Deprecated>
                </EuiPageContent_Deprecated>
                <EuiSpacer />
                <CleaningActivityFeed />
            </EuiPageBody>
        </StyledEuiPage>
    )
}

const mapStateToProps = (state) => {
    return {
        user: state.auth.user
    }
}
export default connect(mapStateToProps)(CleaningJobsHome);