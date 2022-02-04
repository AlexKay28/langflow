import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT,
    SET_MESSAGE
  } from './types'

  import {NotificationManager} from 'react-notifications'
  
  import AuthService from '../services/auth.service'
  
  export const register = (username, email, password) => (dispatch) => {
    return AuthService.register(username, email, password).then(
      (response) => {
        dispatch({
          type: REGISTER_SUCCESS,
        })
  
        dispatch({
          type: SET_MESSAGE,
          payload: response.data.message,
        })

        NotificationManager.success(response.data.message)
  
        return Promise.resolve();
      },
      (error) => {
        const message =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString()
  
        dispatch({
          type: REGISTER_FAIL,
        })
  
        dispatch({
          type: SET_MESSAGE,
          payload: message,
        })

        NotificationManager.error(message)
  
        return Promise.reject();
      }
    )
  }
  
  export const login = (username, password) => (dispatch) => {
    return AuthService.login(username, password).then(
      (data) => {
        dispatch({
          type: LOGIN_SUCCESS,
          payload: { user: data },
        })

        NotificationManager.success('Successfull logging')
  
        return Promise.resolve();
      },
      (error) => {
        const message =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString()
  
        dispatch({
          type: LOGIN_FAIL,
        })
  
        dispatch({
          type: SET_MESSAGE,
          payload: message,
        })

        NotificationManager.error(message)
  
        return Promise.reject()
      }
    )
  }
  
  export const logout = () => (dispatch) => {
    AuthService.logout();
    window.location.pathname = "/login"
  
    dispatch({
      type: LOGOUT,
    })
  }