import React, { useState, useEffect } from 'react';
import { hostNameApi } from 'apis';
import Nipple from './Nipple';
import './App.css';

const App = () => {
  const [nippleData, setNippleData] = useState([]);
  const [hostName, setHostName] = useState('');

  const onChange = ({ degree, distance }) => {
    setNippleData([degree, distance]);
  };

  useEffect(() => {
    console.log(nippleData);
  }, [nippleData]);

  useEffect(() => {
    hostNameApi().then(response => {
      setHostName(response.data);
    });
  }, []);

  return (
    <div className="container">
      <h1 className="host-name">{hostName}</h1>
      <div className="container">
        <Nipple
          onChange={onChange}
          width="250px"
          height="250px"
          options={{
            mode: 'static',
            position: { top: '50%', left: '50%' },
            color: 'black',
          }}
        />
      </div>
    </div>
  );
};

export default App;
