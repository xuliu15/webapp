import React, { useState, useEffect } from "react";
import api from './api';

const App = () => {
  const [population, setPopulation] = useState([]);
  const [formData, setFormdata] = useState({
    count: '',
    date: ''
  });

  useEffect(() => {
    fetchPopulation();
  }, []);

  const fetchPopulation = async () => {
    const response = await api.get('/population/');
    setPopulation(response.data);
  };

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormdata({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/population/', formData);
    fetchPopulation();
    setFormdata({
      count: '',
      date: ''
    });
  };

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Web App
          </a>
        </div>
      </nav>
      <div className="container">
        <form onSubmit={handleFormSubmit}>

          <div className="mb-3 mt-3">
            <label htmlFor="count" className="form-label">
              Count
            </label>
            <input type="text" className="form-control" id='count' name="count" onChange={handleInputChange} value={formData.count}>
            </input>
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>

        </form>

        <table className="table table-striped table-bordered table-hover">
         <thead>
            <tr>
              <th>Count</th>
              <th >Date</th>
              <th>Factorial</th>
            </tr>
         </thead>
         <tbody>
            {population.map((population) => (
              <tr key={population.id}>
                <td>{population.count}</td>
                <td>{population.date}</td>
                <td>{population.factorial}</td>
              </tr>
            ))}
         </tbody>
        </table>


      </div>
    </div>

  );
};

export default App;
