import {SET_USER, UNSET_USER} from '../constants';

const initialState = {};

function userReducer(state = initialState, action) {
  switch (action.type) {
  case SET_USER: {
    const newUser = {...action.data};
    return newUser;
  }
  case UNSET_USER: {
    return {};
  }
  default:
    return state;
  }
}

export default userReducer;