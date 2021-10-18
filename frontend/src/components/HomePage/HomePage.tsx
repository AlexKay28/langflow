import AboutProject from "../AboutProject/AboutProject"
import OurTeam from "../OurTeam/OurTeam"
import GoPractice from "../GoPractice/GoPractice"
import Footer from "../Footer/Footer"

const HomePage = (): JSX.Element => {
    return (
        <>
            <GoPractice/>
            <AboutProject/>
            <OurTeam/>
            <Footer/>
        </>
    );
};

export default HomePage