import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import { withStyles } from '@material-ui/core/styles';
import 'react-awesome-button/dist/styles.css';
import { baseAPIUrl } from "../../store/constants";
import TextResults from "../TextResults"
import Button from '@material-ui/core/Button';
import "./index.css"

const styles = theme => ({
    searchcontainer: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: "400px",
        marginTop: "50px",
    },
    dense: {
        marginTop: 16,
    },
    menu: {
        width: 200,
    },
});


class Search extends Component {
    state = {
        multiline: '',
        texts: []
    }


    firstFetch = () => {
        const myHeaders = new Headers({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${JSON.parse(localStorage.getItem('token'))}`,
        })

        const config = {
            method: 'GET',
            headers: myHeaders,
        };

        fetch(`${baseAPIUrl}search/query/?q=${this.state.multiline}`, config)
            .then(response => response.json())
            .then(data => {
                this.setState({ texts: data.hits })
            })
    }


    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    };


    render() {
        const { classes } = this.props;

        return (
            <div>
                <div className="wrapper">
                    <div className={classes.searchcontainer}>
                        <TextField
                            id="outlined-multiline-flexible"
                            label="Search:"
                            multiline
                            rowsMax="4"
                            value={this.state.multiline}
                            onChange={this.handleChange('multiline')}
                            className={classes.textField}
                            margin="normal"
                            helperText="Please write what you want to search."
                            variant="outlined"
                            type="search"
                        />

                    </div>



                </div>
                <div className="buttonSearch">
                    <Button variant="contained" size="large" color="primary" className={classes.margin}
                        onClick={this.firstFetch}>
                        Search
                  </Button>
                </div>
                <br />

                {this.state.texts.length > 0 ? <TextResults texts={this.state.texts} /> : null}
            </div>
        );
    }
}

export default withStyles(styles)(Search);