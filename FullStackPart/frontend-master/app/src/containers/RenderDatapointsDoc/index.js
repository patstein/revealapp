import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';
import Modal from 'react-responsive-modal';
import "./index.css"

class RenderDatapointsDoc extends Component {
    state = {
        open: false,
        modalText: '',
    };


    componentDidMount = () => {
        let els = Array.prototype.slice.call(document.getElementsByTagName("span"), 1);
        let self = this;
        els.forEach(el => {
            if (el.classList)
                el.classList.add("span-hover");
            else
                el.className += " span-hover";
        });

        els.forEach(el => {
            el.addEventListener('click', (e) => {
                self.setState({ open: true, modalText: e.target.title })
            })
        })
    };
    componentWillUnmount = () => {
        document.removeEventListener('click', this.onHighlichtClick)
    }

    getHTMLOfSelection = () => {
        let range;
        if (document.selection && document.selection.createRange) {
            range = document.selection.createRange();
            return range.htmlText;
        }
        else if (window.getSelection) {
            let selection = window.getSelection();
            if (selection.rangeCount > 0) {
                range = selection.getRangeAt(0);
                let clonedSelection = range.cloneContents();
                let div = document.createElement('div');
                div.appendChild(clonedSelection);
                return div.innerHTML;
            }
            else {
                return '';
            }
        }
        else {
            return '';
        }
    }


    onSelectText = () => {
        let html = this.getHTMLOfSelection();
        this.setState({
            selectedText: html,
        })
    };


    resetSelection = () => {
        this.setState({
            selectedText: ""
        });
        window.getSelection().empty()

    }


    onCloseModal = () => {
        console.log("closing")
        this.setState({ open: false });
    };


    render() {
        return (
            <div className="container">
                <Paper className="datapoints">
                    <div className="textDoc" onMouseUp={this.onSelectText}>
                        <Modal open={this.state.open} onClose={this.onCloseModal} center>
                            <h2>{this.state.modalText}</h2>
                        </Modal>
                        <div dangerouslySetInnerHTML={{ __html: this.props.pdf.text }}>
                        </div>
                    </div>
                </Paper>
            </div>

        );
    }
}

export default RenderDatapointsDoc;
