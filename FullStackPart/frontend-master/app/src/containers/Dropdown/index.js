import React, {Component} from 'react';
import {withStyles} from "@material-ui/core";
import {connect} from 'react-redux';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import {selectedLevel} from './renderLevels';

import {setDatapointsPdfs} from './../../store/actions/pdfActions';
import {fetchKeyPhrasesOfTag, fetchTagsAndDocRefs} from "../../store/actions/tagsActions";
import "./index.css";

const styles = theme => ({
    button: {
        // left: "50%",
        margin: 10,
    },
})

class Dropdown extends Component {
    state = {
        currentTag: {},
        level1Selected: {},
        level2Options: [],
        level2Selected: {},
        level3Options: [],
        level3Selected: {},
    };


    handleChange = option => {
        if (this.props.dropdownHandleChange) {
            this.props.dropdownHandleChange(option);
        } else {
            this.props.fetchTagsAndDocRefs().then((res) => {
                let pdfIndexes = res.data.find(tag => tag.name === option.name).pdf_documents;
                this.props.setDatapointsPdfs(pdfIndexes);
            })
        }
        this.props.fetchKeyPhrasesOfTag(option.id)

    };

    getTag = option => this.props.tags.filter(tag => tag.parent_tag === option.id);

    onLevel1Selected = option => {
        this.setState({
            currentTag: option,
            level1Selected: option,
            level2Options: this.getTag(option),
            level3Options: {},
            level2Selected: {},
            level3Selected: {},
        });
        this.handleChange(option)
    };

    onLevel2Selected = option => {
        this.setState({
            currentTag: option,
            level2Selected: option,
            level3Options: this.getTag(option),
            level3Selected: {}
        });
        this.handleChange(option)
    };

    onLevel3Selected = (option) => {
        this.setState({
            currentTag: option,
            level3Selected: option
        });
        this.handleChange(option)
    };

    renderLevel1 = () => {
        let level1Tags = this.props.tags.filter(tag => tag.parent_tag === null);
        return selectedLevel(level1Tags, this.state.level1Selected, this.onLevel1Selected, 'Tag1')
    };

    renderLevel2 = () => selectedLevel(this.state.level2Options, this.state.level2Selected, this.onLevel2Selected, 'Tag2');
    renderLevel3 = () => selectedLevel(this.state.level3Options, this.state.level3Selected, this.onLevel3Selected, 'Tag3');

    removeTag = () => {
        this.setState({
            currentTag: {},
            level1Selected: {},
            level2Options: [],
            level2Selected: {},
            level3Options: [],
            level3Selected: {},
        });
    }

    render () {

        if (this.props.tags.length > 0) {
            return (
              <div>
                  <h3>Tags</h3>
                  <div className="dropdown">
                      {this.renderLevel1()}
                      {this.renderLevel2()}
                      {this.renderLevel3()}
                  </div>
                  <br>
                  </br>
                  <Divider variant="middle"/>
                  <br>
                  </br>
                  <Typography variant="subheading" color="inherit">
                      Selected Tag:
                  </Typography>
                  <div margintop="5px" style={{backgroundColor: this.state.currentTag.color, borderRadius: '4px'}}>
                      <Paper style={{backgroundColor: this.state.currentTag.color}}>
                          {this.state.currentTag.name}
                      </Paper>

                  </div>


              </div>
            )
        } else {
            return <div>Loading...</div>
        }
    }
}


const mapStateToProps = state => ({tags: state.tags});

const mapDispatchToProps = dispatch => ({
    setDatapointsPdfs: pdfIndexes => dispatch(setDatapointsPdfs(pdfIndexes)),
    fetchKeyPhrasesOfTag: id => dispatch(fetchKeyPhrasesOfTag(id)),
    fetchTagsAndDocRefs: () => dispatch(fetchTagsAndDocRefs()),
});

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Dropdown));