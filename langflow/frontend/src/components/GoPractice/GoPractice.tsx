import Link from '@material-ui/core/Link';
import { makeStyles } from "@material-ui/styles";

export const useStyles = makeStyles(() => ({
	button: {
		padding: "44px 0",
		width: "500px"
	}
}));

const GoPractice = (): JSX.Element => {
    return (
        <div className="p-5">
            <Link href='/question' style={{ fontSize: '36px' }} color="inherit" underline="none" className="btn btn-success">Go practice!</Link>
        </div>
    );
}

export default GoPractice;