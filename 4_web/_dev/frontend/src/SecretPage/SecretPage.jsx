import React from 'react';

import { userService, authenticationService } from '../_services';
import { handleResponse } from '../_helpers';

class SecretPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentUser: authenticationService.currentUserValue,
            contacts: null,
            error: null
        };
    }

    componentDidMount() {
        userService.getSecret()
            .then(handleResponse)
            .then(data => {
                this.setState({ contacts: data.contacts });
            })
            .catch(error => this.setState({ error }));
    }

    render() {
        const { contacts, error } = this.state;
        return (
            <div>
                <h2>All contacts</h2>
                {error &&
                    <div className="alert alert-danger">
                        {error}
                    </div>
                }
                {contacts &&
                    <div className="alert alert-info">
                        {contacts.map((contact) => <div>
                            <ul>
                                <li>Name: {contact.name}</li>
                                <li>Phone: {contact.phone}</li>
                            </ul>
                            <hr></hr>
                        </div>)}
                    </div>
                }
            </div>
        );
    }
}

export { SecretPage };