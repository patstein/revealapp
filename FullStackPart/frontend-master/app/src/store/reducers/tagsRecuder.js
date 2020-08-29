import {SET_TAGS} from '../constants';

const initialState = [];

function tagsReducer (state = initialState, action) {
  switch (action.type) {
    case SET_TAGS: {
      const newTags = [...action.data];
      return newTags;
    }
    default:
      return state;
  }
}

export default tagsReducer;