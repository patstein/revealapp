import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

class Redirect extends React.Component {

  componentDidMount = () => {
    this.props.history.push(this.props.path);
  }

  render() {
    return (
      <div>Redirecting...</div>
    );
  }
}

Redirect.propTypes = {
  history: PropTypes.object.isRequired,
  path: PropTypes.string.isRequired,
};

export default withRouter(connect()(Redirect));