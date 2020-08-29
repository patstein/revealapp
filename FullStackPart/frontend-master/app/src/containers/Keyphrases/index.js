import React, {Component} from 'react';
import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';
import {connect} from 'react-redux';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import "./index.css"

const styles = {
    card: {
        width: "100%",
        marginTop: '2%'
    },
    paper: {
        marginTop: "5%",
        width: "90%",
        padding: "5% 5% 5% 5%",
        background: "#DCDCDC",

    },
    keyphrases: {
        marginTop: "5%",
    }

};

class KeyPhrase extends Component {


    render () {
        const {classes} = this.props;
        const regex = /(<([^>]+)>)/ig

        if (this.props.phrases && this.props.phrases.length !== 0) {
            return (
              <div>
                  <Divider variant="middle"/>
                  <Typography className={classes.keyphrases} variant="subheading" gutterBottom>
                      Keyphrases:
                  </Typography>
                  <div className="keyphraseWrapper">
                      {
                          this.props.phrases.map((phrase, index) => {
                                return phrase.selected_text
                                  ?
                                  <div key={index}>
                                      <Paper className={classes.paper} key={index}>
                                          {phrase.selected_text.replace(regex, "")}
                                      </Paper>
                                  </div>
                                  :
                                  null


                            }
                          )
                      }
                  </div>

                  <br></br>
              </div>
            )
        }
        else {
            return null
        }
    }
}

const mapStateToProps = state => {
    return {
        tags: state.tags,
        phrases: state.phrases.tagPhrases
    };
};
export default connect(mapStateToProps)(withStyles(styles)(KeyPhrase));