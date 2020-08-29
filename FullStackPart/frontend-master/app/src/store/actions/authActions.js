import {SET_TOKEN, UNSET_TOKEN} from '../constants';
import {fetchUser} from './userActions';
import axios from './../../axios_config';
import {fetchTagsAndDocRefs} from "./tagsActions";
import {fetchAllPdfs} from "./pdfActions";

export const setToken = () => {
  const token = JSON.parse(localStorage.getItem('token'));
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
  return {
    type: SET_TOKEN,
    data: token
  };
};

export const unsetToken = () => {
  axios.defaults.headers.common['Authorization'] = undefined;
  return {
    type: UNSET_TOKEN,
  };
};

export const loginUser = credentials => dispatch => {
  const data = {
    username: credentials.username,
    password: credentials.password
  };

  return  axios.post('auth/token/', data)
    .then(res => {
      if (res.data.non_field_errors === undefined) {
        localStorage.setItem('token', JSON.stringify(res.data.access));
        dispatch( setToken());
        dispatch(fetchUser());
        dispatch(fetchTagsAndDocRefs());
        dispatch(fetchAllPdfs());
      }
      return res.data;
    }).catch(error => error.response.data);
};
