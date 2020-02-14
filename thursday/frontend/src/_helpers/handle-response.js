import { authenticationService } from '../_services';

export function handleResponse(response, codes = [401]) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (codes.indexOf(response.status) !== -1) {
                // auto logout if 401 Unauthorized
                authenticationService.logout();
                window.location.reload(true);
            }

            const error = (data && data.detail) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}