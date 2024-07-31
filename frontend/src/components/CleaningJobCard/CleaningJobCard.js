import React from 'react';
import {
    EuiFlexGroup, EuiFlexItem,
    EuiLoadingChart,
    EuiBadge,
    EuiSpacer,
    EuiText,
    EuiButton,
    EuiCard,
} from '@elastic/eui';
import {shallowEqual, useSelector} from 'react-redux';
import styled from 'styled-components';
import moment from "moment";

const ImageHolder = styled.div`
  min-width: 400px;
  min-height: 200px;
  
  & > img {
    position: relative;
    z-index: 2;
  }
`

const cleaningTypeToDisplayNameMapping = {
    dust_up: "Dust Up",
    spot_clean: "Spot Clean",
    full_clean: "Full Clean"
}

export default function CleaningJobCard({
    user,
    isOwner,
    cleaningJob,
    offersError,
    offersIsLoading,
    createOfferForCleaning

}) {
    const userOfferForCleaningJob = useSelector(
        (state) => state.offers.data?.[cleaningJob?.id]?.[user?.id],
        shallowEqual
    )
    const image = (
        <ImageHolder>
            <EuiLoadingChart size="xl" style={{position: "absolute", zIndex: 1}}/>
            <img src="https://cs2.livemaster.ru/storage/6d/56/5c2fb0e5a4b51f643d8340a44fso--kosmetika-ruchnoj-raboty-mylo-olivkovoe.jpg" alt="Cleaning Job Cover"/>
        </ImageHolder>
    )
    const title = (
        <EuiFlexGroup justifyContent="spaceBetween" alignItems="center">
            <EuiFlexItem grow={false}>{cleaningJob.name}</EuiFlexItem>
            <EuiFlexItem grow={false}>
                <EuiBadge color="secondary">
                    {cleaningTypeToDisplayNameMapping[cleaningJob.cleaning_type]}
                </EuiBadge>
            </EuiFlexItem>
        </EuiFlexGroup>
    )
    const footer = (
        <>
            <EuiSpacer />
            <EuiFlexGroup>
                <EuiFlexItem grow={false}>
                    <EuiText>Hourly Rate: ${cleaningJob.price}</EuiText>
                </EuiFlexItem>
                <EuiFlexItem grow={false}>
                    {isOwner || userOfferForCleaningJob ? null : (
                        <EuiButton
                            onClick={() => createOfferForCleaning({ cleaning_id: cleaningJob.id })}
                            isLoading={offersIsLoading}
                        >
                            Offer Services
                        </EuiButton>
                    )}
                </EuiFlexItem>
            </EuiFlexGroup>
        </>
    )
    const betaBadgeLabel = userOfferForCleaningJob
        ? `Offer ${userOfferForCleaningJob.status}`.toUpperCase()
        : null;
    const betaBadgeTooltipContent = userOfferForCleaningJob
        ? `Offer sent on ${moment(new Date(userOfferForCleaningJob.created_at)).format('MMM Do YYYY')}`
        : null;
    return (
        <EuiCard
            display="plain"
            textAlign="left"
            image={image}
            title={title}
            description={cleaningJob.description}
            footer={footer}
            betaBadgeProps={{
                label: betaBadgeLabel,
                tooltipContent: betaBadgeTooltipContent
            }}
        />
    )
}