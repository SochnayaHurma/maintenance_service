import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom';

import {Layout, LandingPage, LoginPage,
    RegistrationPage, ProfilePage, NotFoundPage,
    ProtectedRoute, CleaningJobsPage, CleaningJobsListOrders, Test
} from '../../components';

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<LandingPage/>}/>
                    <Route path="cleaning-jobs/*" element={<ProtectedRoute component={CleaningJobsPage}/>}/>
                    <Route path="cleaning-orders/*" element={<ProtectedRoute component={CleaningJobsListOrders}/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/profile" element={<ProtectedRoute component={ProfilePage}/>}/>
                    <Route path="/registration" element={<RegistrationPage/>}/>
                    <Route path="/test" element={<Test/>}/>
                    <Route path="*" element={<NotFoundPage/>}/>
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;
