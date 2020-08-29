import {isAxiosAuthorized} from "../../helper";
import axios from "../../axios_config";
import {SET_DATAPOINTS_PDFS, SET_ALL_PDFS, SET_ANNOTATION_PDF, SET_DATAPOINTS_PDF} from "../constants";

// Pdfs for Annotation section
export const fetchAllPdfs = () => dispatch => {
    if (!isAxiosAuthorized()) {
        return;
    }

    return axios.get(`file/get/all`)
      .then(res => {
          dispatch(setAllPdfs(res.data))
          return res;
      })
      .catch(err => err.response);
};


export const setAllPdfs = (payload) => {
    return {
        type: SET_ALL_PDFS,
        data: payload
    }
}


// Pdfs for Datapoins section
export const fetchDatapointsPdfs = (indexes) => dispatch => {
    if (!isAxiosAuthorized())
        return;


    let query_param = ''
    indexes.forEach((ind, index) => {
        let newParam = indexes.length - 1 > index ? 'param' + String(index) + '=' + String(ind) + '&' : 'param' + String(index) + '=' + String(ind)
        query_param = query_param + newParam
    })

    return axios.get(`file/get/?${query_param}`)
      .then(res => {
          dispatch(setDatapointsPdfs(res.data))
          return res;
      })
      .catch(err => err.response);
};


export const setDatapointsPdfs = (pdfs_indexes) => {
    return {
        type: SET_DATAPOINTS_PDFS,
        data: pdfs_indexes
    }
}

export const setDatapointsPdf = (pdf) => {
    return {
        type: SET_DATAPOINTS_PDF,
        data: pdf
    }
}


// Pdf for Annotaion section
export const setAnnotationPdf = (pdf) => {
    return {
        type: SET_ANNOTATION_PDF,
        data: pdf
    }
}
