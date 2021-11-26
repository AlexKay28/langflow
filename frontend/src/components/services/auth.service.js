import api from "../../utils/api"

const register = (username, email, password) => {
  return api.post('/authorization', {
    username,
    email,
    password,
  })
};

const login = (username, password, is_anon = false) => {
  return api.post('/login', {
      username,
      password,
      is_anon
    })
    .then((response) => {
      console.log(response.data);
      if (response.data.session_token) {
        localStorage.setItem("user", JSON.stringify(response.data));
        localStorage.setItem("session_token", response.data.session_token);
        localStorage.setItem("username", username);
        localStorage.setItem("password", password);
      }

      return response.data;
    });
};

const logout = () => {
  localStorage.clear();
};

export default {
  register,
  login,
  logout,
};