import axios from 'axios';
import { baseAPIUrl } from './store/constants';

axios.defaults.baseURL = baseAPIUrl;

export default axios;
