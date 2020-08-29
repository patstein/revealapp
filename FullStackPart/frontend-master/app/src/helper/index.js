import axios from './../axios_config.js';

export const handleFetchErrors = (response) => {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
};

export const isAxiosAuthorized = () => {
  if(axios.defaults.headers.common['Authorization'] === undefined) {
    return false;
  }
  return true;
};
