import React from 'react';
import {Helmet} from "react-helmet";
import styled from "styled-components";
import {
    EuiProvider,
    EuiGlobalToastList
} from '@elastic/eui';
import "@elastic/eui/dist/eui_theme_light.css"
import 'assets/css/fonts.css';
import 'assets/css/override.css';

import {Navbar} from "components";
import { useToasts } from "hooks/ui/useToasts";


const StyledLayout = styled.div`
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  background-color: rgb(224, 228, 234);
  display: flex;
  flex-direction: column;
`

const StyledMain = styled.main`
  min-height: calc(100vh - ${(props) => props.theme.euiHeaderHeight} - 1px) !important;
  display: flex;
  flex-direction: column;
  
  & h1 {
    color: ${(props) => props.theme.euiTitleColor} !important;
  }
`


export default function LayOut({children}) {
    const { toasts, removeToast } = useToasts();
    return (
        <React.Fragment>
            <Helmet>
                <meta charSet="utf-8" />
                <title>Phresh Cleaners</title>
                <link rel="canonical" href="http://localhost"/>
            </Helmet>
            <EuiProvider colorMode="light">
                <StyledLayout>
                    <Navbar/>
                    <StyledMain>{children}</StyledMain>
                    <EuiGlobalToastList
                        toasts={toasts}
                        dismissToast={(toastId) => removeToast(toastId)}
                        toastLifeTimeMs={15000}
                        side="right"
                        className="auth-toast-list"
                    />
                </StyledLayout>
            </EuiProvider>
        </React.Fragment>
    )
}