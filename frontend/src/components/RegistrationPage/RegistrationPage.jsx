import { useState, useRef } from "react"
import { useDispatch } from "react-redux"

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

import { register } from "../actions/auth"

const theme = createTheme({
    palette: {
      primary: green,
    }
})

const RegistrationPage = (props) => {
    const form = useRef();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [successful, setSuccessful] = useState(false);

    const dispatch = useDispatch();

    const onChangeUsername = (e) => {
        const username = e.target.value;
        setUsername(username);
    };

    const onChangeEmail = (e) => {
        const email = e.target.value;
        setEmail(email);
    };

    const onChangePassword = (e) => {
        const password = e.target.value;
        setPassword(password);
    };

    const handleRegister = (e) => {
        e.preventDefault();

        setSuccessful(false);

        dispatch(register(username, email, password))
            .then(() => {
            props.history.push("/login")
            setSuccessful(true);
            })
            .catch(() => {
            setSuccessful(false);
            });
    };

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
                                Sign up
                            </Typography>
                            <Box component="form" noValidate onSubmit={handleRegister} ref={form} sx={{ mt: 3 }}>
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
                                        id="email"
                                        label="Email Address"
                                        name="email"
                                        autoComplete="email"
                                        value={email}
                                        onChange={onChangeEmail}
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
                                <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} >
                                    Sign Up
                                </Button>
                                <Grid container justifyContent="flex-end">
                                    <Grid item>
                                        <Link href="/login" variant="body2">
                                        Already have an account? Sign in
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

export default RegistrationPage