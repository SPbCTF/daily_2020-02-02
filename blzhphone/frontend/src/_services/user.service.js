import config from '../config';
import { authHeader, handleResponse } from '../_helpers';

export const userService = {
    getMe, updateMe, getSecret
};

function getMe() {
    const requestOptions = { method: 'GET', headers: authHeader() };
    return fetch(`${config.apiUrl}/api/me`, requestOptions).then(handleResponse);
}

function updateMe(name, phone) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...authHeader()
        },
        body: JSON.stringify({name, phone})
    };
    return fetch(`${config.apiUrl}/api/me`, requestOptions)
}

function getSecret() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    }
    return fetch(`${config.apiUrl}/api/admin`, requestOptions)
}