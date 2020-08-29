import React from 'react';
import ReactDOM from 'react-dom';
import App from './containers/App';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { MuiThemeProvider } from '@material-ui/core/styles';

import './index.css';

import store from './store';

import theme from './theme';

const used_theme = theme;

ReactDOM.render(
    <Provider store={store}>
        <MuiThemeProvider theme={used_theme}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </MuiThemeProvider>
    </Provider>

    ,
    document.getElementById('root')
);
