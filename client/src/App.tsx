import React, { useState } from 'react';
import './App.css';
import { TextField, Button, Alert } from '@mui/material';

const server = import.meta.env.VITE_SERVER_ADDRESS as string

const App: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [userInput, setUserInput] = useState<string>("")
  const [alertText, setAlertText] = useState<string>("")
  const [alert, setAlert] = useState<boolean>(false)


  // Handle requests with distinction between input and server errors
  const fetchData = (userInput: string) => {
    fetch(`${server}/?user_input=${userInput}`)
      .then(response => {
        if (!response.ok) {
          if (response.status == 422) {
            return response.json();
          }
          throw new Error('Network response was not ok.');
        }
        return response.json();
      })
      .then(responseData => {
        if (responseData.error) {
          console.log(responseData)
          setAlertText(responseData.error)
          setAlert(true)
        }
        else {
          setAlertText("");
          setAlert(false);
          setData(responseData);
        }
      })

  };


  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = () => {
    fetchData(userInput);
  };


  return (
    <div className="App">
      <Alert style={{ display: alert ? "block" : "none" }} severity="warning">{alertText}</Alert>

      <h1>{data ? data.data : ""}</h1>
      <div className='input-components'>
        <TextField label="Input"
          value={userInput}
          onChange={handleInputChange}
        />
        <Button
          onClick={handleSubmit}
        >Submit</Button>
      </div>
    </div>
  );
}

export default App;
