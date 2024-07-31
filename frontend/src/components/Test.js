import {connect} from 'react-redux';

import {Actions as cleaningAction} from 'redux/cleanings';
import {Actions as offerAction} from 'redux/offers';
import {useEffect} from "react";

const newCleaningData = {
    newCleaning: {
        name: 'Очистка',
        description: 'Описание ййй',
        price: 20.44,
        cleaning_type: 'spot_clean'
    }
}
const updateCleaningData = {
        name: 'ОчисткаUPDATED3',
        description: 'Описание ййй',
        price: 10.22,
        cleaning_type: 'spot_clean'

}

function Test(
    {
        currentUser,
        listUsers,
        ///
        cleaningData,
        cleaningCreate,
        cleaningGetOne,
        cleaningGetAll,
        cleaningUpdate,
        deleteCleaning,
        ///
        offersData,
        offerCreate,
        offerAccept,
        offerCancel,
    }
) {
    const getOneCLeaningCall = async () => {
        const response = await cleaningGetOne({cleaningId: 2339})
        console.log(response)
    }
    const getAllCleaningCall = async () => {
        const response = await cleaningGetAll();
        // console.log(response)
    }

    const createCleaningCall = async () => {
        const response = await cleaningCreate(newCleaningData);
        console.log(response)
    }
    const updateCleaningCall = async () => {
        const response = await cleaningUpdate({cleaningId: 2328, cleaningUpdate: updateCleaningData});
        console.log(response)
    }

    const deleteCleaningCall = async () => {
        const response = deleteCleaning({cleaningId: 2351})
        console.log(response)
    }

    const offerCreateCall = async () => {
        const response = await offerCreate({cleaningId: 2349});
        console.log(response)
    }
    const offerAcceptCall = async () => {
        const targetId = 2350;
        const targetCLeaning = cleaningData[targetId];
        const targetCleaningOffers = offersData[targetId]
        const response = await offerAccept({cleaningId: targetId, username: listUsers[1].username});
        console.log(response)
    }
    const offerCancelCall = async () => {
        const targetId = 2350;
        const targetCLeaning = cleaningData[targetId];
        const targetCleaningOffers = offersData[targetId]
        const response = await offerCancel({cleaningId: targetId});
        console.log(response)
    }

    useEffect(() => {
        // [1,2,3,4,5].forEach(() => createCleaningCall())
          // createCleaningCall() CREATE CLEANING
          //  updateCleaningCall() // UPDATE CLEANING
          // getOneCLeaningCall() GET ONE CLEANING
        // getAllCleaningCall() GET ALL CLEANING
        // deleteCleaningCall() DELETE ONE CLEANING
        ///////////////////////////////////////////

    }, []);


    return <button onClick={() => offerCancelCall()}>Действие</button>
}

const mapStateToProps = (state) => {
    return {
        currentUser: state.auth.user,
        listUsers: state.auth.users,
        ///
        cleaningData: state.cleaning.data,
        ///
        offersData: state.offers.data,
    }
}
const mapDispatchToProps = {
    cleaningCreate: cleaningAction.createCleaningJob,
    cleaningGetOne: cleaningAction.fetchCleaningJobById,
    cleaningGetAll: cleaningAction.fetchAllUserOwnedJobs,
    cleaningUpdate: cleaningAction.updateCleaningJob,
    deleteCleaning: cleaningAction.deleteCleaningJob,
    //////////////////////////////////
    offerCreate: offerAction.createOfferForCleaning,
    offerAccept: offerAction.acceptUserOfferForCleaningJob,
    offerCancel: offerAction.cancelUserOfferForCleaningJob,

}

export default connect(mapStateToProps, mapDispatchToProps)(Test)