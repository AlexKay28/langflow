import React from "react";
import AboutProject from "../AboutProject/AboutProject"
import OurTeam from "../OurTeam/OurTeam"
import GoPractice from "../GoPractice/GoPractice"
import Footer from "../Footer/Footer"


class HomePage extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
    }

    render() {
        return (
            <>
                <GoPractice/>
                <AboutProject/>
                <OurTeam/>
                <Footer/>
            </>
        );
    }
};

export default HomePage;