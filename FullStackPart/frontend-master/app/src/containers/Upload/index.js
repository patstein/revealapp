import React, { Component } from 'react';
import { FilePond, File, registerPlugin } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';
import "./index.css"
import { baseAPIUrl } from './../../store/constants';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';

registerPlugin(FilePondPluginImageExifOrientation, FilePondPluginImagePreview);


class Upload extends Component {
  state = {
    files: []
  }

  handleInit() {
    console.log('FilePond instance has initialised', this.pond);
  }


  render() {
    const token = localStorage.getItem("token").slice(1, -1)
    console.log(token)
    return (
      <div className="App">
        <Card className="cardUpload" >

          {/* Pass FilePond properties as attributes */}
          <FilePond ref={ref => this.pond = ref}
            allowMultiple={false}
            server=
            {
              {
                url: `${baseAPIUrl}file/upload/`,
                process: {
                  headers: {
                    Authorization: `Bearer ${token}`
                  },
                },
              }
            }
            className="filepond"
            oninit={() => this.handleInit()}

            onupdatefiles={(fileItems) => {
              // Set current file objects to this.state
              this.setState({
                files: fileItems.map(fileItem => fileItem.file)
              });
            }
            }
          >
            {/* Update current files  */}
            {this.state.files.map(file => (
              <File key={file} src={file} origin="local" />
            ))}
          </FilePond>
          <Button variant="contained" color="primary" onClick={() => this.props.history.push('/annotate')} >
            Go to the File Explorer
      </Button>
        </Card>
      </div>
    );
  }
}

export default Upload;
