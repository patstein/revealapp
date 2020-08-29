import {SET_DATAPOINTS_PDFS, SET_ANNOTATION_PDF, SET_ALL_PDFS, SET_DATAPOINTS_PDF} from '../constants';

const initialState = {
    all_pdfs: [],
    datapoint_pdfs: [],  // Array of pdf objects to be displayed in Datapoints section.
    datapoint_pdf: {},
    annotation_pdf: {}  // Single pdf object. The current pdf being annotated.
};

function pdfsReducer (state = initialState, action) {
    switch (action.type) {
        case SET_ALL_PDFS: {
            return {...state, all_pdfs: action.data};
        }
        case SET_DATAPOINTS_PDFS: {
            let pdf_indices = action.data
            let new_datapoint_pdfs = state.all_pdfs.filter(pdf => pdf_indices.includes(pdf.id))
            return {...state, datapoint_pdfs: new_datapoint_pdfs};
        }
        case SET_DATAPOINTS_PDF: {
            return {...state, datapoint_pdf: action.data};
        }
        case SET_ANNOTATION_PDF: {
            return {...state, annotation_pdf: action.data};
        }
        default:
            return state;
    }
}

export default pdfsReducer;