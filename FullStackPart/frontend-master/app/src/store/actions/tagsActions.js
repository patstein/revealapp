import {isAxiosAuthorized} from "../../helper";
import axios from "../../axios_config";
import {SET_TAGS, SET_PHRASES_TAG, SET_PHRASES_PDF} from "./../constants";


export const fetchTagsAndDocRefs = () => dispatch => {
    if (!isAxiosAuthorized())
        return;

    return axios.get('tags/')
      .then(res => {
          dispatch(setTags(res.data))
          return res
      })
      .catch(err => {
          return err.response
      });
};

export const setTags = (payload) => {
    return {
        type: SET_TAGS,
        data: payload
    }
}


export const fetchKeyPhrasesOfTag = (tag_id) => dispatch => {
    if (!isAxiosAuthorized())
        return;

    return axios.get(`tags/phrases/${tag_id}/`)
      .then(res => {
          dispatch(setPhrasesofTag(res.data))
          return res
      })
      .catch(err => {
          return err.response
      });
};

export const setPhrasesofTag = (payload) => {
    return {
        type: SET_PHRASES_TAG,
        data: payload
    }
}

export const unsetPhrasesofTag = () => {
    return {
        type: SET_PHRASES_TAG,
        data: []
    }
}

export const fetchKeyPhrasesOfPdf = (pdf_id) => dispatch => {
    if (!isAxiosAuthorized())
        return;

    return axios.get(`tags/pdfs/phrases/${pdf_id}/`)
      .then(res => {
          dispatch(setPhrasesofPdf(res.data))
          return res
      })
      .catch(err => {
          return err.response
      });
};

export const setPhrasesofPdf = (payload) => {
    return {
        type: SET_PHRASES_PDF,
        data: payload
    }
}



