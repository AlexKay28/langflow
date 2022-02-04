import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Redirect } from 'react-router-dom'

import Button from '@material-ui/core/Button'
import CssBaseline from '@material-ui/core/CssBaseline'
import TextField from '@material-ui/core/TextField'
import Link from '@material-ui/core/Link'
import Grid from '@material-ui/core/Grid'
import Box from '@material-ui/core/Box'
import Typography from '@material-ui/core/Typography'
import Container from '@material-ui/core/Container'
import { makeStyles } from '@material-ui/styles'

import { login } from '../actions/auth'

const useStyles = makeStyles({
    button: {
        '&.MuiButton-root': { 
            fontSize: 22, 
            minWidth: 170, 
            height: 60,
            backgroundColor: '#023866',
            marginTop: 28
        }
    },
    header: {
        '&.MuiTypography-root': {
            color: '#023866',
            fontSize: 46
        }
    },
    textField: {
        '& .MuiInputLabel-root': {
            color: '#023866',
            top: '-2px',
            backgroundColor: 'ghostwhite',
            padding: '0 9px'
        },
        '& .MuiOutlinedInput-notchedOutline': {
            border: '2px solid #023866'
        },
        '& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#023866'
        }
    },
    link: {
        '&.MuiTypography-root': {
            color: '#73738D',
            textDecoration: 'none',
            fontWeight: 600,
            fontSize: 18
        }
    }
})

const LoginPage = (props) => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const classes = useStyles()

    const { isLoggedIn } = useSelector(state => state.auth)

    const dispatch = useDispatch()

    const onChangeUsername = (e) => {
        const username = e.target.value
        setUsername(username)
    }

    const onChangePassword = (e) => {
        const password = e.target.value
        setPassword(password)
    }

    const handleLogin = (e) => {
        e.preventDefault()

        dispatch(login(username, password))
    }

    if (isLoggedIn) {
        return <Redirect to="/home" />
    }

    return (
        <div className="vh-90">
            <div className="centered-element">
                <Container component="main" maxWidth="xs">
                    <CssBaseline />
                    <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center'
                    }}
                    >
                        <Typography className={classes.header} component="h1" variant="h5">
                            Sign in
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleLogin}>
                            <Grid container>
                                <Grid item xs={12} sx={{mt: 4}}>
                                    <TextField
                                    className={classes.textField}
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
                                <Grid item xs={12} sx={{mt: 4}}>
                                    <TextField
                                    className={classes.textField}
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
                            <Button type="submit" fullWidth variant="contained" className={classes.button}>
                                Sign In
                            </Button>
                            <Grid container justifyContent="flex-end">
                                <Grid item style={{margin: '10px auto'}}>
                                    <Link href="/registration" variant="body2" className={classes.link} >
                                    New user? Sign up to create your account
                                    </Link>
                                </Grid>
                            </Grid>
                        </Box>
                    </Box>
                </Container>
            </div>
        </div>
    )
}

export default LoginPage