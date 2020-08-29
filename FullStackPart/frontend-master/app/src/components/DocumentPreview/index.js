import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import Typography from '@material-ui/core/Typography';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import { withRouter } from 'react-router-dom';
import { connect } from "react-redux"

const styles = {
  card: {
    width: "100%",
    marginTop: '2%'
  }
};

class DocumentPreview extends Component {

  buttonHandler = () => {
    this.props.history.push(`/annotate/${this.props.pdf.id}`)
  }

  render() {
    const { classes } = this.props;

    return (
      <Card className={classes.card}>
        <CardContent>
          <Typography variant="body1" gutterBottom>
            {this.props.pdf.pdf.split('/').reverse()[0]}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small" color="primary" onClick={this.buttonHandler}>
            Open
          </Button>
        </CardActions>
      </Card>

    );
  }
}


export default withRouter(withStyles(styles)(connect()(DocumentPreview)))