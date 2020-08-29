import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Logout from './../Logout';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';


function TabContainer(props) {
    return (
        <Typography component="div" style={{ padding: 8 * 3 }}>
            {props.children}
        </Typography>
    );
}

TabContainer.propTypes = {
    children: PropTypes.node.isRequired,
};
const styles = theme => ({
    root: {
        flexGrow: 1,
        width: '100%',
        zIndex: 10
        // position: 'fixed',
        // top: '0px',

    },
    toolbar: {
        alignItems: 'space-between',

    },
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: 0,
        marginRight: 0,
    },
})

class Header extends Component {

    state = {
        url: this.props.location.pathname,
    };

    render() {
        const { classes } = this.props;
        const { url } = this.state;

        return (
            <div className={classes.root}>

                <AppBar position="static" color="primary" className={classes.toolbar}>
                    <Toolbar variant="dense">
                        <Typography variant="headline" color="inherit" className={classes.grow}>
                            Document Annotation
                      </Typography>
                        {localStorage.getItem("token") ? <Logout /> :
                            <Button color="inherit" onClick={() => this.props.history.push('/login')}>Login</Button>}

                    </Toolbar>
                </AppBar>
                <Paper>
                    {localStorage.getItem("token") ?
                        <Tabs
                            value={url}
                            onChange={this.handleChange}
                            indicatorColor="primary"
                            textColor="primary"
                            centered
                        >
                            <Tab label="Homepage" value="/" />
                            <Tab label="Search" value="/search" />
                            <Tab label="Upload" value="/upload" />
                            <Tab label="Datapoints" value="/datapoints" />
                            <Tab label="Annotate" value="/annotate" />
                        </Tabs>
                        : null}
                </Paper>

            </div>
        );
    }

    handleChange = (event, value, state) => {
        this.props.history.push(value)
        this.setState({ url: value })
    };
}

Header.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(Header));
