import React, {Component} from 'react';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import TextField from '@material-ui/core/TextField';
import PropTypes from 'prop-types';
import 'react-awesome-button/dist/styles.css';
import {withStyles} from '@material-ui/core/styles';
import {AwesomeButton} from 'react-awesome-button';

import Error from '../Error/';
import {loginUser} from '../../store/actions/authActions';
import {styles} from "./theme";
import './index.css'

class Login extends Component {
   state = {
      username: '',
      password: '',
      redirect: false,
      error: ''
    };

  handleUsernameInput = e => this.setState({username:e.target.value});
  handlePasswordInput = e => this.setState({password: e.target.value});
  loginError = (error) => this.setState({error});

  userLogin = e => {
    e.preventDefault();
    this.props.login(this.state, this);
    this.setState({username: '', password: '', redirect: true});
  };

  render () {
      const classes = this.props.classes;
      const {error, username, password} = this.state;

      return (
      <form className="Login-Form" onSubmit={this.userLogin}>
        <Error error={error}/>
        <TextField
          id="username"
          label="Username"
          className={classes.textField}
          placeholder="Enter your Username"
          value={username}
          onChange={this.handleUsernameInput}
        /><br/>
        <TextField
          id="password"
          label="Password"
          className={classes.textField}
          type="password"
          placeholder="Enter your Password"
          value={password}
          onChange={this.handlePasswordInput}
        /><br/>
        <AwesomeButton
          type="secondary"
          size="large"
          onClick={this.userLogin}>
          Login
        </AwesomeButton>
      </form>
    );
  }
}

Login.propTypes = {
  classes: PropTypes.object.isRequired,
  history: PropTypes.object.isRequired,
};

const mapStateToProps = state => ({
    currentUser: state.currentUser,
    token: state.token,
});

const mapDispatchToProps =  (dispatch, ownProps) => ({
    login: async (userData, self) => {
        console.log("the self", self);
        const data = await dispatch(loginUser(userData));
        data.non_field_errors === undefined ? ownProps.history.push('/') : self.loginError(data.non_field_errors[0])
    }
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Login)));
