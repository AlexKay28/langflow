import React from "react";

class Footer extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
    }

    render() {
        return (
            <footer className="text-white-50">
                <div>Service created by <a href="https://github.com/AlexKay28" className="text-white">AlexKay</a> and <a href="https://github.com/Alkhimovmv" className="text-white">AlkhimovMV</a>.</div>
            </footer>
        );
    }
};

export default Footer;