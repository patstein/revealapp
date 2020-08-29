import axios from './../../axios_config';
import { isAxiosAuthorized } from './../../helper';

import {SET_USER, UNSET_USER} from '../constants';

export const setUser = userData => {
  return {
    type: SET_USER,
    data: userData
  };
};

export const unsetUser = () => {
  localStorage.clear();
  return {
    type: UNSET_USER,
  };
};

export const fetchUser = () => dispatch => {
  if(!isAxiosAuthorized())
    return;

  return axios.get('user/info/')
    .then(res => {
      const action = setUser(res.data);
      dispatch(action);
      return res;
    })
    .catch(err => err.response);
};

