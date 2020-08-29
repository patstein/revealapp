import React, {Component} from 'react';
import Paper from '@material-ui/core/Paper';
import Sidebar from '../Sidebar'
import {withRouter} from 'react-router-dom';
import {connect} from 'react-redux';

import "./index.css"
import {fetchAllPdfs, setAnnotationPdf} from "../../store/actions/pdfActions";

class RenderAnnotationDoc extends Component {

    state = {
        selectedText: "",
        startOfSelection: -2
    };

    componentDidMount = () => {
        this.props.dispatch(fetchAllPdfs())
          .then(() => {
              let pdf = this.props.pdfs.filter(pdf => pdf.id === Number(this.props.match.params.pdfId))[0]
              this.props.dispatch(setAnnotationPdf({...pdf}))
          })


    };

    componentWillUnmount = () => {
        this.props.dispatch(setAnnotationPdf({}))
    }

    componentDidUpdate = () => {
        let pdf = this.props.pdfs.filter(pdf => pdf.id === Number(this.props.match.params.pdfId))[0]
        this.props.dispatch(setAnnotationPdf({...pdf}))
        document.getElementById('roots').innerHTML = this.props.pdf.text
    };

    shouldComponentUpdate = (nextProps, nextState) => {
        if (this.getHTMLOfSelection()) {
            return true
        }
        let nextPdf = nextProps.pdfs.filter(pdf => pdf.id === Number(this.props.match.params.pdfId))[0];
        return nextPdf.text !== this.props.pdf.text;
    }

    getStartofSelection = () => {
        if (window.getSelection) {
            let sel = window.getSelection();
            let div = document.getElementById("roots");

            if (sel.rangeCount) {
                // Get the selected range
                let range = sel.getRangeAt(0);


                // Create a range that spans the content from the start of the div
                // to the start of the selection
                let precedingRange = document.createRange();
                precedingRange.setStartBefore(div.firstChild);
                precedingRange.setEnd(range.startContainer, range.startOffset);

                // Get the text preceding the selection and do a crude estimate
                // of the number of words by splitting on white space
                let textPrecedingSelection = precedingRange.toString();
                let wordIndex = textPrecedingSelection.split('').length//.split(/\s+/).length;
                console.log("wordIndex", wordIndex)
                // alert(wordIndex)
                return wordIndex;
            }
        }
        return -2
    }

    getHTMLOfSelection = () => {
        let range;
        if (document.selection && document.selection.createRange) {
            range = document.selection.createRange();
            return range.htmlText;
        }
        else if (window.getSelection) {
            let selection = window.getSelection();
            if (selection.rangeCount > 0) {
                range = selection.getRangeAt(0);
                let clonedSelection = range.cloneContents();
                let div = document.createElement('div');
                div.appendChild(clonedSelection);
                return div.innerHTML;
            }
            else {
                return '';
            }
        }
        else {
            return '';
        }
    };


    onSelectText = () => {
        let startOfSelection = this.getStartofSelection()
        let html = this.getHTMLOfSelection();
        this.setState({
            selectedText: html,
            startOfSelection: startOfSelection,
        })
    };


    resetSelection = () => {
        this.setState({
            selectedText: "",
            startOfSelection: -2
        });
        window.getSelection().empty()
    };


    render () {
        console.log("djhsfjshdlf", this.state.startOfSelection)
        return (
          <div className="container">
              <div>
                  <Paper className="leftPanel">
                      <div className="textDoc" onMouseUp={this.onSelectText}>
                          <div id="roots">
                          </div>
                      </div>
                  </Paper>
              </div>

              <div className="rightPanel">
                  <Sidebar selectedText={this.state.selectedText} startOfSelection={this.state.startOfSelection}
                           pdf={this.props.pdf} resetSelection={this.resetSelection}/>
              </div>

          </div>
        );

    }


}


const mapStateToProps = state => {
    return {
        tags: state.tags,
        pdf: state.pdfs.annotation_pdf,
        pdfs: state.pdfs.all_pdfs
    };
};

export default withRouter(connect(mapStateToProps)(RenderAnnotationDoc));
