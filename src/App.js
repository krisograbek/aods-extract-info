import React, {useState, useEffect} from 'react';
import './App.css';

function App() {
  const [customText, setCustomText] = useState([]);
  const [info, setInfo] = useState([]);

  // useEffect(() => {
  //   fetch('/info').then(
  //     res => res.json()).then(
  //       data => {
  //         console.log(" Info ")
  //         setInfo(data.infos);
  //       }
  //     );
  // }, [])

  useEffect(() => {
    fetch('/text').then(
      res => res.json()).then(
        data => {
          console.log(" HEYAH ")
          setCustomText(data.text);
          console.log(customText)
        }
      );
  }, [])

  return (
    <div className="App">
      {/* <header className="App-header"> */}
        Books, Podcasts, ...
        {customText.map((item, i) => (
          <div key={i}>
          <p>Episode: {item.title} </p>
          <ol>
          {item.sents.map((sent, idx) => (
            <li key={idx}>{sent}</li>
          ))}
          </ol>
          </div>
        ))}
        
      {/* </header> */}
    </div>
  );
}

export default App;
