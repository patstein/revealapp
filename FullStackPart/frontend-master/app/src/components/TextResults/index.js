import React, {Component} from 'react';
import {withStyles} from "@material-ui/core/styles";
import Paper from '@material-ui/core/Paper';
import {withRouter} from 'react-router';
import {connect} from 'react-redux';

import "./index.css"

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
    },
});

const paperStyle = {
    margin: '50px auto',
    padding: '20px 20px 20px 20px',
    width: '70%',
};


class TextResults extends Component {

    handleClick = (pdfName) => {
        let pdfNameEnd = pdfName.split('/').reverse()[0]
        let pdfsNames = this.props.pdfs.map(pdf => {
            return {
                ...pdf,
                pdf: pdf.pdf.split('/').reverse()[0]
            }
        })
        let matchArr = pdfsNames.filter(pdf => pdf.pdf === pdfNameEnd)
        if (matchArr.length === 1) {
            let pdfId = matchArr[0].id
            this.props.history.push(`/annotate/${pdfId}`);

        } else {
            this.props.history.push(`/annotate/`);
        }
    }

    render () {
        const {texts} = this.props;
        let textListContent;
        let textarr = [];
        texts.forEach(ele => {
            ele.highlight.text.forEach(text => {
                textarr.push({pdf: ele._source.pdf, text: text})
            })
        })
        console.log('textarr', textarr);


        if (texts) {
            textListContent = (
              <div className="result">
                  {
                      textarr.map(t => (
                        <Paper style={paperStyle} className="box" elevation={10}
                               onClick={() => this.handleClick(t.pdf)}>
                            <h6>{t.pdf}</h6>
                            {<p dangerouslySetInnerHTML={{__html: t.text}}/>}
                        </Paper>
                      ))
                  }
              </div>
            )
        } else {
            textListContent = null;
        }
        return (
          <div>
              {textListContent}
          </div>
        );
    }
}

const mapStateToProps = state => ({
    pdfs: state.pdfs.all_pdfs,
});

export default withStyles(styles)(withRouter(connect(mapStateToProps)(TextResults)));