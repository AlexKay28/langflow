import { SET_MESSAGE, CLEAR_MESSAGE } from './types'

export const setMessage = function(message) {
  return ({
    type: SET_MESSAGE,
    payload: message,
  })
}

export const clearMessage = function() {
  return ({
    type: CLEAR_MESSAGE,
  })
}