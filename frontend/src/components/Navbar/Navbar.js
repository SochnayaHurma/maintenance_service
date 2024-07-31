import React, {useState} from 'react';
import {
    EuiIcon,
    EuiAvatar,
    EuiHeader,
    EuiHeaderSection,
    EuiHeaderSectionItem,
    EuiHeaderSectionItemButton,
    EuiLink,
    EuiPopover,
    EuiHeaderLink,
    EuiHeaderLinks,
    EuiFlexGroup, EuiFlexItem,
} from '@elastic/eui';
import {Link, useNavigate} from 'react-router-dom';
import styled from 'styled-components';
import { connect } from "react-redux";

import { Actions as authActions } from '../../redux/auth'
import loginIcon from 'assets/img/loginIcon.svg';
import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { UserAvatar} from "components";

const LogoSection = styled(EuiHeaderLink)`
  padding: 0 2rem !important;
  text-decoration: none !important;
`
const StyledEuiHeaderSectionItem = styled(EuiHeaderSectionItem)`
  border-right: solid 1px rgba(0, 0, 0, 0.09);
`

const StyledEuiHeaderLink = styled(EuiHeaderLink)`
  text-decoration: none !important;
  border: none;
  background-color: white;
  color: dodgerblue !important;
`

const StyledEuiHeaderSectionItemButton = styled(EuiHeaderSectionItemButton)`
  background-color: ${(props) => props.theme.euiColorGhost};
  border-radius: 50% !important;
  height: ${(props) => props.theme.euiSizeL} !important;
  width: ${(props) => props.theme.euiSizeL} !important;
  align-self: center !important;
`

const AvatarMenu = styled.div`
  display: flex;
  justify-content: space-between;
  min-width: 300px;
  
  & .avatar-actions {
    margin-left: 2rem;
  }
`

const StyledEuiPopover = styled(EuiPopover)`
  align-self: center;
`


export default function Navbar() {
    const [avatarMenuOpen, setAvatarMenuOpen] = useState(false);
    const { user, logUserOut } = useAuthenticatedUser();
    const toggleAvatarMEnu = () => setAvatarMenuOpen(!avatarMenuOpen);
    const closeAvatarMenu = () => setAvatarMenuOpen(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        closeAvatarMenu();
        logUserOut();
        navigate("/");
    }

    const avatarButton = (
        <StyledEuiHeaderSectionItemButton
            aria-label="User avatar"
            onClick={() => user?.profile && toggleAvatarMEnu()}
        >
            {
                user?.profile ? (
                    <UserAvatar
                     size="l"
                     user={user}
                     initialsLength={2}
                    />
                ) : (
                    <Link to="/login">
                        <EuiAvatar size="l" color="#1E90FF" name="user" imageUrl={loginIcon}/>
                    </Link>
                )
            }
        </StyledEuiHeaderSectionItemButton>
    );

    const renderAvatarMenu = () => {
        if (!user?.profile) return null;
        return (
            <AvatarMenu>
                <UserAvatar
                size="xl"
                user={user}
                initialsLength={2}
                />

                <EuiFlexGroup direction="column" className="avatar-actions">
                    <EuiFlexItem grow={1}>
                        <p>
                            {user.email} - {user.username}
                        </p>
                    </EuiFlexItem>
                    <EuiFlexItem grow={1}>
                        <EuiFlexGroup justifyContent="spaceBetween">
                            <EuiFlexItem grow={1}>
                                <Link to="/profile">Profile</Link>
                            </EuiFlexItem>
                            <EuiFlexItem grow={1}>
                                <EuiLink href="#" onClick={() => handleLogout()}>Log out</EuiLink>
                            </EuiFlexItem>
                        </EuiFlexGroup>
                    </EuiFlexItem>
                </EuiFlexGroup>
            </AvatarMenu>
        )
    }
    return (
        <EuiHeader >
            <EuiHeaderSection>
                <StyledEuiHeaderSectionItem>
                    <LogoSection href='/'>
                        <EuiIcon type='cloudDrizzle' color='#1E90FF' size='l'/> Phresh
                    </LogoSection>
                </StyledEuiHeaderSectionItem>
                <StyledEuiHeaderSectionItem>
                    <EuiHeaderLinks aria-label='app navigation links'>
                        <StyledEuiHeaderLink iconType='tear' onClick={() => navigate("/cleaning-orders")}>My offers</StyledEuiHeaderLink>
                        <StyledEuiHeaderLink iconType='tear' href='#'>Find Cleaners</StyledEuiHeaderLink>
                        <StyledEuiHeaderLink iconType='tag' onClick={() => navigate("/cleaning-jobs")}>Find Jobs</StyledEuiHeaderLink>
                        <StyledEuiHeaderLink iconType='help' href='#'>Help</StyledEuiHeaderLink>
                    </EuiHeaderLinks>
                </StyledEuiHeaderSectionItem>
            </EuiHeaderSection>
            <EuiHeaderSection>
                <StyledEuiPopover
                    id="avatar-menu"
                    isOpen={avatarMenuOpen}
                    closePopover={closeAvatarMenu}
                    anchorPosition="downRight"
                    button={avatarButton}
                    panelPaddingSize="l"
                >
                    {renderAvatarMenu()}
                </StyledEuiPopover>
            </EuiHeaderSection>
        </EuiHeader>
    )
}