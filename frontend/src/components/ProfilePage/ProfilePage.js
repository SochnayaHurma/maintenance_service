import React from 'react';
import { connect } from "react-redux";
import styled from "styled-components";
import moment from "moment";
import {
    EuiAvatar,
    EuiTitle,
    EuiText,
    EuiIcon,
    EuiHorizontalRule,
    EuiPage,
    EuiPageHeader,
    EuiPageHeaderSection,
    EuiPageContentBody_Deprecated,
    EuiPageBody,
    EuiPageContent_Deprecated,

} from '@elastic/eui';

import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { UserAvatar } from "components";

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
  display: flex;
  justify-content: center;
  flex: 1;
`

const StyledEuiPageContentBody = styled(EuiPageContentBody_Deprecated)`
  display: flex;
  flex-direction: column;
  align-items: center;
  
  & h2 {
    margin-bottom: 1rem;
    font-weight: unset;
  }
`

export default function ProfilePage(){
    const { user } = useAuthenticatedUser();
    return (
        <StyledEuiPage>
            <EuiPageBody component="section">
                <StyledEuiPageHeader>
                    <StyledEuiPageHeaderSection>
                        <EuiTitle size="l">
                            <h1>Профиль</h1>
                        </EuiTitle>
                    </StyledEuiPageHeaderSection>
                </StyledEuiPageHeader>
                <EuiPageContent_Deprecated verticalPosition="center" horizontalPosition="center">
                    <StyledEuiPageContentBody>
                        <UserAvatar
                            size="xl"
                            user={user}
                            initialsLength={2}
                        />
                        <EuiTitle>
                            <h2>@{user.username}</h2>
                        </EuiTitle>
                        <EuiText>
                            <p>
                                <EuiIcon type="email"/> {user.email}
                            </p>
                            <p>
                                <EuiIcon type="clock"/> member since {moment(user.created_at).format("MM-DD-YYYY")}
                            </p>
                            <p>
                                <EuiIcon type="alert"/> {" "}
                                {user.profile.full_name ? user.profile.full_name : "Full name not specified."}
                            </p>
                            <p>
                                <EuiIcon type="number" /> {" "}
                                {user.profile.phone_number ? user.profile.phone_number : "No phone number added."}
                            </p>
                            <EuiHorizontalRule/>
                            <p>
                                <EuiIcon type="quote" /> {" "}
                                {user.profile.bio ? user.profile.bio : "This user hasn't written a bio yet."}
                            </p>
                        </EuiText>
                    </StyledEuiPageContentBody>
                </EuiPageContent_Deprecated>
            </EuiPageBody>
        </StyledEuiPage>
    )
}