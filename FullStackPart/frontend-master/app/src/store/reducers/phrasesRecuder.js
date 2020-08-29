import {SET_PHRASES_TAG, SET_PHRASES_PDF} from '../constants';

const initialState = {
    tagPhrases: [],
    pdfPhrases: []
};

function phrasesReducer (state = initialState, action) {
    switch (action.type) {
        case SET_PHRASES_TAG: {
            const newState = {
                tagPhrases: [...action.data],
                pdfPhrases: state.pdfPhrases
            }
            return newState;
        }
        case SET_PHRASES_PDF: {
            const newState = {
                tagPhrase: state.tagPhrases,
                pdfPhrases: [...action.data]
            }
            return newState;
        }
        default:
            return state;
    }
}


export default phrasesReducer;