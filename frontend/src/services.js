import axios from 'axios';

const getEndpoint = (path) => {
  return `http://localhost:8000/${path}/`;
};

export function registerUser(data) {
  return axios.post(getEndpoint('accounts/signup'), data);
}