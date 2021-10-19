import React from 'react'
import Link from '@material-ui/core/Link'
import { makeStyles } from "@material-ui/styles"
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import FormControl from '@material-ui/core/FormControl'
import Select, { SelectChangeEvent } from '@material-ui/core/Select'
import api from "../../utils/api";

export const useStyles = makeStyles(() => ({
	button: {
		padding: "44px 0",
		width: "500px"
	}
}));

const GoPractice = (): JSX.Element => {
    const [firstLanguage, setFirstLanguage] = React.useState<string>('');
    const [secondLanguage, setSecondLanguage] = React.useState<string>('');
    const [level, setLevel] = React.useState<string>('');
    const [openLevel, setOpenLevel] = React.useState(false);
    const [openFirstLanguage, setOpenFirstLanguage] = React.useState(false);
    const [openSecondLanguage, setOpenSecondLanguage] = React.useState(false);
  
    const handleChangeFirstLanguage = (event: SelectChangeEvent<typeof firstLanguage>) => {
        setFirstLanguage(event.target.value);
    };

    const handleChangeSecondLanguage = (event: SelectChangeEvent<typeof secondLanguage>) => {
        setSecondLanguage(event.target.value);
    };

    const handleChangeLevel = (event: SelectChangeEvent<typeof level>) => {
        setLevel(event.target.value);
    };

    const handleClick = () => {
        const dataConfig = {
            first_language: firstLanguage,
            second_language: secondLanguage,
            level: level
        }
        api.post(`/configure?first_language=${dataConfig.first_language}&second_language=${dataConfig.second_language}&level=${dataConfig.level}`, JSON.stringify(dataConfig))
            .then(response => {
                window.localStorage.setItem('dataUuid', JSON.stringify(response.data))
            })
            .catch((error) => {
                console.log(error);
            });
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
        <div >
            <div className="p-5">
                <FormControl className="bg-light" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="first-language-label">Language</InputLabel>
                    <Select
                    labelId="first-language-label"
                    id="first_language"
                    open={openFirstLanguage}
                    onClose={handleCloseFirstLanguage}
                    onOpen={handleOpenFirstLanguage}
                    value={firstLanguage}
                    label="First language"
                    onChange={handleChangeFirstLanguage}
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
                    value={secondLanguage}
                    label="Second language"
                    onChange={handleChangeSecondLanguage}
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
                <Link href='/question' style={{ fontSize: '36px' }} color="inherit" underline="none" className="btn btn-success" onClick={handleClick}>Go practice!</Link>
            </div>
        </div>
    );
}

export default GoPractice;