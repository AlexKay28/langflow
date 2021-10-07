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
                <div className="h-100 text-center text-white bg-dark">
                    <GoPractice/>
                    <AboutProject/>
                    <OurTeam/>
                    <Footer/>
                </div>
            </>
        );
    }
};

export default HomePage;