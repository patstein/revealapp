import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

import png from "./jacob.png"



const styles = {
    root: {
        width: '100%',
        maxWidth: 500,
        marginTop: 100,
    },
};

class Homepage extends Component {
    render() {
        const { classes } = this.props;

        return (
            <div className='homepage'>

                <div className={classes.root}>
                    <div className="image">
                        <img src={png} alt="jacob" width="100px" left="50%" />
                    </div>
                    <Typography variant="display2" gutterBottom>
                        Welcome to Jacob
                    </Typography>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(Homepage);