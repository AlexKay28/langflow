import React from 'react'
import Button from '@material-ui/core/Button'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import FormControl from '@material-ui/core/FormControl'
import Select, { SelectChangeEvent } from '@material-ui/core/Select'
import api from "../../utils/api"
import { createTheme, ThemeProvider } from '@material-ui/core/styles'
import green from '@material-ui/core/colors/green'

const theme = createTheme({
    palette: {
      primary: green,
    }
})

const GoPractice = (props: any): JSX.Element => {
    const [firstLanguage, setFirstLanguage] = React.useState<string>('english');
    const [secondLanguage, setSecondLanguage] = React.useState<string>('russian');
    const [level, setLevel] = React.useState<string>('0');
    const [openLevel, setOpenLevel] = React.useState(false);
    const [openFirstLanguage, setOpenFirstLanguage] = React.useState(false);
    const [openSecondLanguage, setOpenSecondLanguage] = React.useState(false);
    const loggedIn = localStorage.getItem("user");
  
    const handleChangeFirstLanguage = (event: SelectChangeEvent<typeof firstLanguage>) => {
        setFirstLanguage(event.target.value);
    };

    const handleChangeSecondLanguage = (event: SelectChangeEvent<typeof secondLanguage>) => {
        setSecondLanguage(event.target.value);
    };

    const handleChangeLevel = (event: SelectChangeEvent<typeof level>) => {
        setLevel(event.target.value);
    };

    const handleClick = async () => {
        var loginData
        if (loggedIn) {
            loginData = {
                username: localStorage.getItem("username"),
                password: localStorage.getItem("password"),
                is_anon: false
            }
        } else {
            loginData = {
                username: '',
                password: '',
                is_anon: true
            }
            const response: any = await api.post('/login', loginData)
            const { session_token } = response.data
            window.localStorage.setItem('session_token', session_token)
        }
        window.localStorage.setItem('firstLanguage', firstLanguage)
        window.localStorage.setItem('secondLanguage', secondLanguage)
        window.localStorage.setItem('level', level)
        window.location.pathname = "/question"
    };

    const handleCloseFirstLanguage = () => {
        setOpenFirstLanguage(false);
    };
  
    const handleOpenFirstLanguage = () => {
        setOpenFirstLanguage(true);
    };

    const handleCloseSecondLanguage = () => {
        setOpenSecondLanguage(false);
    };
  
    const handleOpenSecondLanguage = () => {
        setOpenSecondLanguage(true);
    };
  
    const handleCloseLevel = () => {
        setOpenLevel(false);
    };
  
    const handleOpenLevel = () => {
        setOpenLevel(true);
    };

    return (
        <div className="p-2 text-center">
            <ThemeProvider theme={theme}>
                <FormControl className="bg-light" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="first-language-label">Language</InputLabel>
                    <Select
                    labelId="first-language-label"
                    id="first_language"
                    open={openFirstLanguage}
                    onClose={handleCloseFirstLanguage}
                    onOpen={handleOpenFirstLanguage}
                    label="First language"
                    onChange={handleChangeFirstLanguage}
                    defaultValue={'english'}
                    >
                    <MenuItem value={'english'}>English</MenuItem>
                    <MenuItem value={'russian'}>Russian</MenuItem>
                    <MenuItem value={'french'}>French</MenuItem>
                    <MenuItem value={'ukrainian'}>Ukrainian</MenuItem>
                    </Select>
                </FormControl>
                <FormControl className="bg-light" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="second-language-label">Language</InputLabel>
                    <Select
                    labelId="second-language-label"
                    id="second_language"
                    open={openSecondLanguage}
                    onClose={handleCloseSecondLanguage}
                    onOpen={handleOpenSecondLanguage}
                    label="Second language"
                    onChange={handleChangeSecondLanguage}
                    defaultValue={'russian'}
                    >
                    <MenuItem value={'english'}>English</MenuItem>
                    <MenuItem value={'russian'}>Russian</MenuItem>
                    <MenuItem value={'french'}>French</MenuItem>
                    <MenuItem value={'ukrainian'}>Ukrainian</MenuItem>
                    </Select>
                </FormControl>
                <FormControl className="bg-light" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="level-label">Level</InputLabel>
                    <Select
                    labelId="level-label"
                    id="level"
                    open={openLevel}
                    onClose={handleCloseLevel}
                    onOpen={handleOpenLevel}
                    value={level}
                    label="Level"
                    onChange={handleChangeLevel}
                    >
                    <MenuItem value={0}>All levels</MenuItem>
                    <MenuItem value={1}>1</MenuItem>
                    <MenuItem value={2}>2</MenuItem>
                    </Select>
                </FormControl>
                <Button type="submit" variant="contained" sx={{ fontSize: 34 }} onClick={handleClick}>
                {loggedIn ? "Go practice!" : "Go practice without registration"}
                </Button>
            </ThemeProvider>
        </div>
    );
}

export default GoPractice;