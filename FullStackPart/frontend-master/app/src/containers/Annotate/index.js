import React, {Component} from 'react';
import {connect} from "react-redux"
import PropTypes from 'prop-types';

import {fetchAllPdfs} from "../../store/actions/pdfActions";
import DocumentPreview from "../../components/DocumentPreview";
import "./index.css";

class Annotate extends Component {

  componentDidMount () {
    this.props.dispatch(fetchAllPdfs())
  }

  render () {
    return (
      <div className="annotate-container">
        {
          Object.values(this.props.pdfs).reverse().map((pdf, index) => {
              return <DocumentPreview key={index} pdf={pdf}/>;
            }
          )}

      </div>
    );
  }
}

const mapStateToProps = state => {
  return ({
    pdfs: state.pdfs.all_pdfs,
  })
}

Annotate.propTypes = {
  pdfs: PropTypes.array
};


export default connect(mapStateToProps)(Annotate);