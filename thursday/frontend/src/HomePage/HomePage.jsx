import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';

import { userService } from '../_services';

class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: null
        };
    }

    componentDidMount() {
        userService.getMe().then(user => this.setState({ user }));
    }

    render() {
        const { user } = this.state;
        return (
            <div>
                <Formik
                    enableReinitialize={true}
                    initialValues={{
                        name: user?.name ?? '',
                        username: user?.username ?? '',
                        level: user?.level ?? 0,
                        phone: user?.phone ?? ''
                    }}
                    validationSchema={Yup.object().shape({
                        name: Yup.string().required(),
                        phone: Yup.string().required(),
                        password: Yup.string(),
                    })}
                    onSubmit={({ name, phone }, { setStatus, setSubmitting }) => {
                        userService.updateMe(name, phone)
                            .then(
                                user => {
                                    const { from } = this.props.location.state || { from: { pathname: "/" } };
                                    this.props.history.push(from);
                                    setSubmitting(false);
                                }
                            )
                            .catch(error => {
                                setSubmitting(false);
                                    setStatus(error);
                            });
                    }}>
                    {({ errors, status, touched, isSubmitting, values }) => (
                        <Form>
                            <div className="form-group">
                                <label htmlFor="name">Name</label>
                                <Field name="name" value={values.name} type="text" className={'form-control' + (errors.name && touched.name ? ' is-invalid' : '')} />
                                <ErrorMessage name="name" component="div" className="invalid-feedback" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="username">Username</label>
                                <Field disabled name="username" value={values.username} type="text" className='form-control'/>
                            </div>
                            <div className="form-group">
                                <label htmlFor="level">Level</label>
                                <Field disabled name="level" value={values.level} type="text" className='form-control'/>
                            </div>
                            <div className="form-group">
                                <label htmlFor="phone">Phone</label>
                                <Field name="phone" value={values.phone} type="text" className={'form-control' + (errors.phone && touched.name ? ' is-invalid' : '')} />
                                <ErrorMessage name="name" component="div" className="invalid-feedback" />
                            </div>
                            <div className="form-group">
                                <button type="submit" className="btn btn-primary" disabled={isSubmitting}>Update</button>
                                {isSubmitting &&
                                    <img alt="loading" src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==" />
                                }
                            </div>
                            {status &&
                                <div className={'alert alert-danger'}>{status}</div>
                            }
                        </Form>
                    )}
                </Formik>
            </div>
        );
    }
}

export { HomePage };