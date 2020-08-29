import {SET_TOKEN, UNSET_TOKEN} from '../constants';

const initialState = null;

function tokenReducer(state = initialState, action) {
  switch (action.type) {
  case SET_TOKEN: {
    const newToken = action.data;
    return newToken;
  }
  case UNSET_TOKEN: {
    let newToken = state;
    newToken = null;
    return newToken;
  }
  default:
    return state;
  }
}

export default tokenReducer;
