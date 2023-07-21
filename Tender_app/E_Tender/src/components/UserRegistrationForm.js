import React, { useState } from 'react';
import axios from 'axios';

const UserRegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
  });

  const { username, email, password, password2 } = formData;

  const onChange = (event) =>
    setFormData({ ...formData, [event.target.name]: event.target.value });

  const onSubmit = async (event) => {
    event.preventDefault();
    if (password !== password2) {
      console.log('Passwords do not match');
    } else {
      const newUser = {
        username,
        email,
        password,
      };
      try {
        const config = {
          headers: {
            'Content-Type': 'application/json',
          },
        };
        const body = JSON.stringify(newUser);
        const res = await axios.post('/api/register/', body, config);
        console.log(res.data);
      } catch (err) {
        console.error(err.response.data);
      }
    }
  };

  return (
    <form onSubmit={(event) => onSubmit(event)}>
      <div>
        <label>Username:</label>
        <input
          type="text"
          name="username"
          value={username}
          onChange={(event) => onChange(event)}
          required
        />
      </div>
      <div>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={email}
          onChange={(event) => onChange(event)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          name="password"
          value={password}
          onChange={(event) => onChange(event)}
          minLength="8"
          required
        />
      </div>
      <div>
        <label>Confirm Password:</label>
        <input
          type="password"
          name="password2"
          value={password2}
          onChange={(event) => onChange(event)}
          minLength="8"
          required
        />
      </div>
      <input type="submit" value="Register" />
    </form>
  );
};

export default UserRegistrationForm;