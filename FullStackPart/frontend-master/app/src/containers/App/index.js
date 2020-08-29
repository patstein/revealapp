import React, {Component} from 'react';
import {connect} from 'react-redux';
import {withRouter, Route, Switch} from 'react-router-dom';
import Header from './../Header'
import Login from './../Login'
import Datapoints from './../../components/Datapoints';
import Search from './../../components/Search';
import Upload from "../Upload"
import './index.css';
import RenderAnnotationDoc from '../RenderAnnotationDoc';
import Annotate from "../Annotate"
import {setToken, unsetToken} from '../../store/actions/authActions';
import {fetchUser, unsetUser} from '../../store/actions/userActions';
import {fetchTagsAndDocRefs} from "../../store/actions/tagsActions";
import {fetchAllPdfs} from "../../store/actions/pdfActions";
import Homepage from '../../components/Homepage';

class App extends Component {


    componentDidMount = () => {
        let plannedRoute = this.props.location.pathname;
        if (!this.props.token) {
            let isTokenInLocalStorage = false;
            try {
                isTokenInLocalStorage = localStorage.getItem('token');
            }
            catch (e) {
                isTokenInLocalStorage = false;
            }
            if (isTokenInLocalStorage) {
                this.props.dispatch(setToken());
                this.props.dispatch(fetchUser())
                  .then(response => {
                      if (response.status === 401) {
                          this.props.dispatch(unsetUser());
                          this.props.dispatch(unsetToken());
                          this.props.history.push('/login');
                      } else {
                          this.props.dispatch(fetchTagsAndDocRefs())
                          this.props.dispatch(fetchAllPdfs())
                          if (plannedRoute.indexOf(plannedRoute.match(/^string:([0-9]+)$/)) !== null) {
                              this.props.history.push('/annotate');
                          } else {
                              this.props.history.push(plannedRoute);
                          }
                      }
                  });
            } else {
                this.props.history.push('/login')
            }
        }
        else {
            this.props.dispatch(fetchUser())
              .then(response => {
                  if (response.status === 401) {
                      this.props.dispatch(unsetUser());
                      this.props.dispatch(unsetToken());
                      this.props.history.push('/login');
                  } else {
                      this.props.dispatch(fetchTagsAndDocRefs())
                      this.props.dispatch(fetchAllPdfs())
                  }
              });
        }
    }

    render () {
        if (this.props.token) {
            return (
              <div className="App">
                  <Header/>
                  <Switch>
                      <Route exact path="/" component={Homepage}/>
                      <Route exact path="/search" component={Search}/>
                      <Route exact path="/upload" component={Upload}/>
                      <Route exact path="/datapoints" component={Datapoints}/>
                      <Route exact path="/annotate" component={Annotate}/>
                      <Route exact path="/annotate/:pdfId/" component={RenderAnnotationDoc}/>
                      <Route render={() => <p>404 - Page not found!</p>}/>
                  </Switch>
              </div>
            )
        }
        else {
            return (
              <div className="App">
                  <Header/>
                  <Switch>
                      <Route path="/login" component={Login}/>
                  </Switch>
              </div>
            )
        }
    };

}

const mapStateToProps = (state) => {
    return {
        token: state.token,
    };
};

export default withRouter(connect(mapStateToProps)(App));
