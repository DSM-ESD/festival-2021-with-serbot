import client from './client';

export const hostNameApi = () => client.get('/hostname');
export const joysticApi = ({ degree, distance }) =>
  client.post('/joystic', { degree, distance });
