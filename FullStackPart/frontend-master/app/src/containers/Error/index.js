import React from 'react';
import './index.css';
import PropTypes from 'prop-types';

const Error = (props) => {
  return (
    <div className="Error">
      {props.error}
    </div>
  );
};
Error.propTypes = {
  error: PropTypes.string,
};
export default Error;
