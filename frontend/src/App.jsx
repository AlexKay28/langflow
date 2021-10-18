import React from "react"
import CurrentPage from "./components/CurrentPage/CurrentPage"
import Header from "./components/Header/Header"

import "./App.css"

class App extends React.Component {
  render() {
    return (
      <>
        <Header/>
        <CurrentPage/>
      </>
    );
  }
}

export default App
