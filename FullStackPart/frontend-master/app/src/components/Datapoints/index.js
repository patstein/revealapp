import React, {Component} from 'react';
import Dropdown from "../../containers/Dropdown";
import KeyPhrase from "../../containers/Keyphrases"
import {connect} from "react-redux";
import Paper from '@material-ui/core/Paper';
import DatapointsDocumentPreview from './../DatapointsDocumentPreview';
import RenderDatapointsDoc from './../../containers/RenderDatapointsDoc';

import "./index.css"


class Datapoints extends Component {
    componentDidMount = () => {
        console.log("componentDidMount Datapoints")
    };

    render () {
        console.log("Rendering Datapoints", this.props)
        return (
          <div className="container">
              <div className="container-datapoints">
                  <div>
                      <Paper className="leftPanel-datapoints">
                          <Dropdown/>
                          {/*Put below into own component*/}

                          <h3>Documents</h3>
                          <div className="documents">
                              {     // When clicking a new tag higlight are still the old ones
                                  this.props.highlights.length > 0 ?
                                    Object.values(this.props.pdfs).reverse().map((pdf, index) => {
                                          if (this.props.highlights.filter((highlight) => highlight.pdf_documents === pdf.id).length > 0) {
                                              let flag = this.props.highlights.filter((highlight) => highlight.pdf_documents === pdf.id)[0]
                                              return <DatapointsDocumentPreview key={index} pdf={pdf}
                                                                                is_doc={flag.all_doc_tagged}/>;
                                          } else {
                                              return <DatapointsDocumentPreview key={index} pdf={pdf}
                                                                                is_doc={true}/>;
                                          }
                                      }
                                    )
                                    :
                                    null
                              }
                          </div>

                          {/*Until here*/}
                          <KeyPhrase/>
                      </Paper>
                  </div>
                  <div className="rightPanel-datapoints">
                      {
                          Object.keys(this.props.pdf).length > 0 ?
                            <div className="text">
                                <RenderDatapointsDoc pdf={this.props.pdf}/>
                            </div>
                            : null
                      }
                  </div>
              </div>
          </div>
        );
    }
}


const mapStateToProps = state => {
    return {
        tags: state.tags,
        pdfs: state.pdfs.datapoint_pdfs,
        pdf: state.pdfs.datapoint_pdf,
        highlights: state.phrases.tagPhrases
    };
};

export default connect(mapStateToProps)(Datapoints);
