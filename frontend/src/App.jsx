import { Component } from 'react'
import CurrentPage from './components/CurrentPage/CurrentPage'
import { NotificationContainer } from 'react-notifications'
import 'react-notifications/lib/notifications.css'

class App extends Component {
  render() {
    return (
      <>
        <NotificationContainer/>
        <CurrentPage/>
      </>
    )
  }
}

export default App
