import React, {useEffect} from 'react';
import {connect, shallowEqual, useSelector} from 'react-redux';
import {
    EuiLoadingSpinner,
    EuiPage,
    EuiPageBody,
    EuiFlexGroup,
    EuiFlexItem,
    EuiAvatar,
    EuiTitle,
    EuiButtonEmpty,
    EuiButtonIcon,
    EuiPageContent_Deprecated, EuiPageContentBody_Deprecated,
} from '@elastic/eui';
import {Routes, Route, useNavigate, useParams} from "react-router-dom";
import styled from 'styled-components';
import {CleaningJobCard, CleaningJobEditForm,
    CleaningJobOffersTable,
    NotFoundPage, PermissionsNeeded, UserAvatar
} from "components";
import { useSingleCleaningJob } from "hooks/cleanings/useSingleCleaningJob";


const StyledEuiPage = styled(EuiPage)`
  flex: 1;

`

const StyledFlexGroup = styled(EuiFlexGroup)`
  padding: 1rem;
`

const StyledEuiPageContent_Deprecated = styled(EuiPageContent_Deprecated)`
  width: 50% !important;
`

const StyledEuiPageContentBody_Deprecated = styled(EuiPageContentBody_Deprecated)`
  //width: 30%;
`

export default function CleaningJobView() {
    const navigate = useNavigate();
    const {cleaningId} = useParams();
    const {
        cleaningJob,
        error,
        isUpdating,
        isLoading,
        activeCleaningId,
        userIsOwner
    } = useSingleCleaningJob(cleaningId);



    if (isLoading) return <EuiLoadingSpinner size="xl"/>
    if (!cleaningJob && activeCleaningId !== cleaningId) return <NotFoundPage/>


    const editJobButton = userIsOwner ? (
        <EuiButtonIcon iconType="documentEdit" aria-label='edit' onClick={() => navigate('edit')}/>
    ) : null;
    const goBackButton = (
        <EuiButtonEmpty
            iconType="sortLeft"
            size="s"
            onClick={() => navigate(`/cleaning-jobs/${cleaningJob.id}`)}
        >
            Назад к услуге
        </EuiButtonEmpty>
    )
    const viewCleaningJobElement = (
        <CleaningJobCard
            offersIsLoading={null}
            cleaningJob={cleaningJob}
            isOwner={userIsOwner}
            createOfferForCleaning={null}
            userOfferForCleaningJob={null}
        />
    )
    const editCleaningJobElement = (
      <PermissionsNeeded
        element={<CleaningJobEditForm cleaningId={cleaningId} />}
        isAllowed={userIsOwner}
      />
    );
    const cleaningJobOffersTableElement = userIsOwner ? (
        <CleaningJobOffersTable
            offers={[]}
            offersUpdating={null}
            offersLoading={null}
        />
    ) : null;
    return (
        <StyledEuiPage>
            <EuiPageBody component="section">
                <StyledEuiPageContent_Deprecated verticalPosition="center" horizontalPosition="center" paddingSize="none">
                    <StyledFlexGroup alignItems="center" direction="row" responsive={false}>
                        <EuiFlexGroup
                            justifyContent="flexStart"
                            alignItems="center"
                            direction="row"
                            responsive={false}
                        >
                            <EuiFlexItem grow={false}>
                                <UserAvatar
                                    size="xl"
                                    user={cleaningJob.owner}
                                    initialsLength={2}
                                />
                            </EuiFlexItem>
                            <EuiFlexItem>
                                <EuiTitle>
                                    <p>@{cleaningJob.owner?.username}</p>
                                </EuiTitle>
                            </EuiFlexItem>
                        </EuiFlexGroup>
                        <EuiFlexItem grow={false}>
                            <Routes>
                                <Route path="/" element={editJobButton}/>
                                <Route path="/edit" element={goBackButton}/>
                            </Routes>
                        </EuiFlexItem>
                    </StyledFlexGroup>
                    <StyledEuiPageContentBody_Deprecated>
                        <Routes>
                            <Route path="/" element={viewCleaningJobElement}/>
                            <Route path="/edit" element={editCleaningJobElement}/>
                            <Route path='*' element={<NotFoundPage/>}/>
                        </Routes>
                    </StyledEuiPageContentBody_Deprecated>
                </StyledEuiPageContent_Deprecated>
                <Routes>
                    <Route path="/" element={cleaningJobOffersTableElement}/>
                </Routes>
            </EuiPageBody>
        </StyledEuiPage>
    )
}
