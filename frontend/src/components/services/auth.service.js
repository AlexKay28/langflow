import api from '../../utils/api'

const register = async (username, email, password) => {
  try {
    const response = await api.post('/authorization', {
      username,
      email,
      password,
    })
    console.log(response);
    if (response.data.status !== 200) {
      throw new Error(response.data.message)
    }
    return response
  } catch (err) {
    throw err
  }
}

const login = async (username, password, is_anon = false) => {
  try {
    const response = await api.post('/login', {
      username,
      password,
      is_anon
    })
    if (response.data.status !== 200) {
      throw new Error(response.data.message)
    }
    if (response.data.session_token) {
      localStorage.setItem("user", JSON.stringify(response.data))
      localStorage.setItem("session_token", response.data.session_token)
      localStorage.setItem("username", username)
      localStorage.setItem("password", password)
    }
  } catch (err) {
    throw err
  }
}

const logout = () => {
  localStorage.clear()
}

export default {
  register,
  login,
  logout,
}