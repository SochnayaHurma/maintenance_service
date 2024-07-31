import React from 'react';
import {
    EuiCommentList,
    EuiText,
    EuiFlexGroup,
    EuiFlexItem,
    EuiBadge,
    EuiButtonIcon,
    EuiButtonEmpty,
    EuiLoadingSpinner,
    EuiMarkdownFormat,
} from '@elastic/eui';
import styled from 'styled-components';
import moment from 'moment';
import 'moment/locale/ru';
import {useNavigate} from "react-router-dom";

import {formatPrice, truncate} from 'utils/format';
import {UserAvatar} from 'components';
import {shallowEqual, connect} from "react-redux";
import {Actions as feedActions} from "../../redux/feed";

moment.locale("ru")
const Wrapper = styled.div`
  width: 100%;
  max-width: 800px;
  margin: 2rem auto;
`
const DescriptionWrapper = styled.div`
  margin-bottom: 1rem;
`
const cleaningTypeToDisplayNameMapping = {
    dust_up: "Очистка пыли",
    spot_clean: "Очистка пятен",
    full_clean: "Полная уборка"
}

const renderTimeStamp = (feedItem) => `${moment(feedItem.created_at).format('Do MMMM, YYYY')}`;
const renderFeedItemAction = (feedItem, navigate) => {
    return <EuiButtonIcon
        title="Перейти на услугу"
        aria-label="Перейти на услугу"
        color="primary"
        iconType="popout"
        onClick={() => navigate(`/cleaning-jobs/${feedItem.id}`)}
    />
}
const renderUpdateEvent = (feedItem) => (
    <EuiFlexGroup responsive={false} alignItems="center" gutterSize="s">
        <EuiFlexItem grow={false}>
            <span>
                обновил(а) услугу <strong>{feedItem.name}.</strong>
            </span>
        </EuiFlexItem>
        <EuiFlexItem grow={false}>
            <EuiBadge className="hide-mobile" color="primary">
                {cleaningTypeToDisplayNameMapping[feedItem.cleaning_type]}
            </EuiBadge>
        </EuiFlexItem>
        <EuiFlexItem grow={false}>
            <EuiBadge className="hide-mobile" color="secondary">
                {formatPrice(feedItem.price)}
            </EuiBadge>
        </EuiFlexItem>
    </EuiFlexGroup>
)
const renderTimelineIcon = (feedItem) => <UserAvatar user={feedItem.owner} size="l"/>
const renderFeedItemBody = (feedItem) => (
    <EuiText size="s">
        <h3>{feedItem.name}</h3>
        <DescriptionWrapper>
            <EuiMarkdownFormat>{truncate(feedItem.description, 300, true)}</EuiMarkdownFormat>
            <p>
                Стоимость: <strong>{formatPrice(feedItem.price)}</strong>
            </p>
        </DescriptionWrapper>
    </EuiText>
)

const createUiElementFromFeedItem = (feedItem, navigate) => {
    const isCreateEvent = feedItem["event_type"] === "is_create";
    return {
        username: feedItem.owner?.username,
        timestamp: renderTimeStamp(feedItem),
        actions: renderFeedItemAction(feedItem, navigate),
        event: isCreateEvent ? `создал(а) новую услугу. ` : renderUpdateEvent(feedItem),
        type: isCreateEvent ? "regular" : "update",
        // timelineAvatar: isCreateEvent ? renderTimelineIcon(feedItem) : null,
        timelineAvatar: renderTimelineIcon(feedItem),
        children: isCreateEvent ? renderFeedItemBody(feedItem) : null
    }
}

class CleaningActivityFeed extends React.Component {
    state = {
        isFetching: false
    }

    componentDidMount() {
        this.setState((state) => ({isFetching: true}));
    }
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.isFetching !== this.state.isFetching) {
            this.props.fetchFeedItems();
        }
    }
    render()
    {
        const {isLoading, feedItems, hasNext, fetchFeedItems, navigate} = this.props;
        // const navigate = useNavigate();
        //
        // const feedItemsElements = useMemo(() => (
        //     feedItems ? feedItems.map((feedItem) => createUiElementFromFeedItem(feedItem, navigate)) : []
        // ), [feedItems, navigate]);
        const handleLoadMore = () => {
            const startingDate = feedItems[feedItems.length - 1].event_timestamp;
            fetchFeedItems(startingDate);
        }
        const renderHasNextButton = () => {
            return hasNext ? (
                <EuiButtonEmpty onClick={handleLoadMore}>Посмотреть ещё..</EuiButtonEmpty>
            ) : (
                <EuiButtonEmpty isLoading={false} isDisabled={true}>
                    {isLoading ? `Загрузка...` : `Ничего больше нет...`}
                </EuiButtonEmpty>
            )
        }
        const feedItemsElements = feedItems ? feedItems.map((feedItem) => createUiElementFromFeedItem(feedItem, navigate)) : []

        return (
            <Wrapper>
                <EuiCommentList
                    comments={feedItemsElements}
                />
                {isLoading ? <EuiLoadingSpinner size="xl"/> : null}
                {renderHasNextButton()}
            </Wrapper>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        isLoading: state.feed.isLoading,
        error: state.feed.error, shallowEqual,
        feedItems: state.feed.data?.cleaning,
        hasNext: state.feed.hasNext.cleaning,
    }
}
const mapDispatchToProps = {
    fetchFeedItems: feedActions.fetchCleaningFeedItem
}

function MapNavigateHook (props) {
    const navigate = useNavigate();
    return <CleaningActivityFeed {...props} navigate={navigate}/>
}
export default connect(mapStateToProps, mapDispatchToProps)(MapNavigateHook)