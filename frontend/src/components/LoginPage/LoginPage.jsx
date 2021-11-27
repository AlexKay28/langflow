import { useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Redirect } from 'react-router-dom'

import Button from '@material-ui/core/Button'
import CssBaseline from '@material-ui/core/CssBaseline'
import TextField from '@material-ui/core/TextField'
import Link from '@material-ui/core/Link'
import Grid from '@material-ui/core/Grid'
import Box from '@material-ui/core/Box'
import Typography from '@material-ui/core/Typography'
import Container from '@material-ui/core/Container'
import { createTheme, ThemeProvider } from '@material-ui/core/styles'
import green from '@material-ui/core/colors/green'

import { login } from "../actions/auth"

const theme = createTheme({
    palette: {
      primary: green,
    }
})

const LoginPage = (props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const { isLoggedIn } = useSelector(state => state.auth);

    const dispatch = useDispatch();

    const onChangeUsername = (e) => {
        const username = e.target.value;
        setUsername(username);
    };

    const onChangePassword = (e) => {
        const password = e.target.value;
        setPassword(password);
    };

    const handleLogin = (e) => {
        e.preventDefault();

        setLoading(true);

        dispatch(login(username, password))
            .then(() => {
            props.history.push("/home")
            window.location.reload();
            })
            .catch(() => {
            setLoading(false);
            });
    };

    if (isLoggedIn) {
        return <Redirect to="/home" />;
    }

    return (
        <div className="vh-100">
            <div className="centered-element">
                <ThemeProvider theme={theme}>
                    <Container component="main" maxWidth="xs">
                        <CssBaseline />
                        <Box
                        sx={{
                            marginTop: 8,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                        >
                            <Typography component="h1" variant="h5">
                                Sign in
                            </Typography>
                            <Box component="form" noValidate onSubmit={handleLogin} sx={{ mt: 3 }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <TextField
                                        style={{
                                            backgroundColor: "white"
                                        }}
                                        variant="filled"
                                        required
                                        fullWidth
                                        id="username"
                                        label="Username"
                                        name="username"
                                        autoComplete="username"
                                        value={username}
                                        onChange={onChangeUsername}
                                        />
                                    </Grid>
                                    <Grid item xs={12}>
                                        <TextField
                                        style={{
                                            backgroundColor: "white"
                                        }}
                                        variant="filled"
                                        required
                                        fullWidth
                                        name="password"
                                        label="Password"
                                        type="password"
                                        id="password"
                                        autoComplete="new-password"
                                        value={password}
                                        onChange={onChangePassword}
                                        />
                                    </Grid>
                                </Grid>
                                <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}
                                >
                                Sign In
                                </Button>
                                <Grid container justifyContent="flex-end">
                                    <Grid item>
                                        <Link href="/registration" variant="body2">
                                        New user? Sign up to create your account
                                        </Link>
                                    </Grid>
                                </Grid>
                            </Box>
                        </Box>
                    </Container>
                </ThemeProvider>
            </div>
        </div>
    );
}

export default LoginPage