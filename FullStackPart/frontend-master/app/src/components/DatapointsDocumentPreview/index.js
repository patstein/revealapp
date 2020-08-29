import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import classNames from 'classnames';
import {loadCSS} from 'fg-loadcss/src/loadCSS';
import {withRouter} from 'react-router-dom';
import Icon from '@material-ui/core/Icon';
import {connect} from "react-redux"
import {setDatapointsPdf} from './../../store/actions/pdfActions';
import Paper from '@material-ui/core/Paper';

import "./index.css"

const styles = {
    card: {},

};

class DatapointsDocumentPreview extends Component {

    clickHandler = () => {
        this.props.dispatch(setDatapointsPdf(this.props.pdf))
    }

    render () {
        console.log("Render DatapointsDocumentPreview")

        const {classes} = this.props;
        return (
          <div>
              <Paper className="card" onClick={this.clickHandler}>
                  {/*<Typography variant="body1" gutterBottom>*/}
                  {this.props.pdf.pdf.split('/').reverse()[0]}
                  <div className="icon">
                      {

                          this.props.is_doc
                            ?
                            <div>
                                <br></br>
                                <Icon className={classNames(classes.icon, "far fa-file-pdf")}/>
                            </div>
                            :
                            <div>
                                <br></br>
                                <Icon className={classNames(classes.icon, 'fas fa-quote-right')}/>
                            </div>

                      }
                  </div>
                  {/*</Typography>*/}
              </Paper>
              <br></br>
          </div>
        );
    }

    componentDidMount () {
        console.log("componentDidMount DatapointsDocumentPreview")
        loadCSS(
          'https://use.fontawesome.com/releases/v5.1.0/css/all.css',
          document.querySelector('#insertion-point-jss'),
        );
    }
}

const mapStateToProps = state => {
    return {
        tags: state.tags,
        highlights: state.highlights
    };
};


export default withRouter(connect(mapStateToProps)(withStyles(styles)(DatapointsDocumentPreview)));