import React, {Component} from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import {unsetToken} from '../../store/actions/authActions';
import {unsetUser} from '../../store/actions/userActions';

const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
    backgroundColor: 'white',
    '&:hover': {
      background: 'blanchedalmond',
    }
  },
});


class Logout extends Component {

  constructor(props) {
    super(props);
    this.classes = props.classes;
  }

  onLogout = () => {
    let action = unsetUser();
    this.props.dispatch(action);
    action = unsetToken();
    this.props.dispatch(action);
    this.props.history.push('/login');
  }

  render() {
    return (
      <Button onClick={this.onLogout} color="inherit">Logout</Button>
    );
  }
}


Logout.propTypes = {
  classes: PropTypes.object,
  history: PropTypes.object,
  dispatch: PropTypes.func,
};

export default withRouter(connect()(withStyles(styles)(Logout)));
