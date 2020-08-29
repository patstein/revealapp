export const SET_TOKEN = 'SET_TOKEN';
export const UNSET_TOKEN = 'UNSET_TOKEN';
export const SET_USER = 'SET_USER';
export const UNSET_USER = 'UNSET_USER';
export const SET_TAGS = 'SET_TAGS';
export const SET_DATAPOINTS_PDFS = 'SET_DATAPOINTS_PDFS';
export const SET_DATAPOINTS_PDF = 'SET_DATAPOINTS_PDF';
export const SET_ANNOTATION_PDF = 'SET_ANNOTATION_PDF';
export const SET_ALL_PDFS = 'SET_ALL_PDFS';
export const SET_PHRASES_TAG = 'SET_PHRASES_TAG';
export const SET_PHRASES_PDF = 'SET_PHRASES_PDF';
export const SET_HL = 'SET_HL';

let baseUrl;
if (process.env.NODE_ENV === 'development') {
    baseUrl = 'http://localhost:8875';
} else {
    baseUrl = 'https://jacob.propulsion-learn.ch';
}
export {
    baseUrl
};

let baseAPIUrl;
if (process.env.NODE_ENV === 'development') {
    baseAPIUrl = 'http://localhost:8875/backend/';
} else {
    baseAPIUrl = 'http://167.172.101.50/backend/';
}
export {
    baseAPIUrl
};

