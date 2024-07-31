import React from 'react';
import {
    EuiPage,
    EuiPageBody,
    EuiPageContent_Deprecated,
    EuiPageContentBody_Deprecated,
    EuiPanel,
    EuiText,
    EuiPageTemplate,
    EuiFlexGroup,
    EuiFlexItem,
} from '@elastic/eui';
import styled from 'styled-components';
import {Carousel, CarouselTitle} from "../../components";
import heroGirl from '../../assets/img/HeroGirl.svg';
import dorm from '../../assets/img/Bed.svg';
import bedroom from '../../assets/img/Bedroom.svg';
import bathroom from '../../assets/img/Bathroom.svg';
import livingRoom from '../../assets/img/Living_room_interior.svg';
import kitchen from '../../assets/img/Kitchen.svg';
import readingRoom from '../../assets/img/Reading_room.svg';
import tvRoom from '../../assets/img/Tv_room.svg';
import {useCarousel} from "../../hooks/ui/useCarousel";

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`

const LandingTitle = styled.h1`
  font-size: 3.5rem !important;
  margin: 2.3rem 0;
  font-weight: unset !important;
`

const StyledEuiPageContent = styled(EuiPageContent_Deprecated)`
  border-radius: 50% !important;
`


const StyledEuiPageContentBody = styled(EuiPageContentBody_Deprecated)`
  max-width: 400px;
  max-height: 400px;
  & > img {
    width: 100%;
    border-radius: 50%;
    margin-block-end: 0 !important;
  }
`

const carouselItems = [
    {label: "dorm room",content: <img src={dorm} alt="bed" />},
    {label: "bedroom",content: <img src={bedroom} alt="bedroom" />},
    {label: "bathroom",content: <img src={bathroom} alt="bathroom" />},
    {label: "living room",content: <img src={livingRoom} alt="living room" />},
    {label: "kitchen",content: <img src={kitchen} alt="kitchen" />},
    {label: "reading room",content: <img src={readingRoom} alt="reading room" />},
    {label: "tv room",content: <img src={tvRoom} alt="tv room" />}
]

export default function LandingPage(props) {
    const { current } = useCarousel(carouselItems, 3000)
    return (
        <EuiPageTemplate>
            <EuiPageBody component="section">
                <EuiFlexGroup direction="column" alignItems="center">
                    <EuiFlexItem>
                        <LandingTitle>Phresh Cleaners</LandingTitle>
                    </EuiFlexItem>
                    <EuiFlexItem>
                        <CarouselTitle items={carouselItems} current={current}/>
                    </EuiFlexItem>
                </EuiFlexGroup>
                <EuiFlexGroup direction="rowReverse">
                    <EuiFlexItem>
                        <Carousel items={carouselItems} current={current}/>
                    </EuiFlexItem>
                    <EuiFlexItem>
                        <StyledEuiPageContent horizontalPosition="center" verticalPosition="center">
                            <StyledEuiPageContentBody >
                                <img src={heroGirl} alt="girl"/>
                            </StyledEuiPageContentBody>
                        </StyledEuiPageContent>
                    </EuiFlexItem>
                </EuiFlexGroup>
            </EuiPageBody>
        </EuiPageTemplate>
    )
}