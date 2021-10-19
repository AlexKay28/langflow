import avatar_alexkay from "../../images/avatar_alexkay.png"
import avatar_alkhimovmv from "../../images/avatar_alkhimovmv.png"
import "./ourteam.scss"

const OurTeam = (): JSX.Element => {
    return (
        <div className="py-5 our_team">
            <div className="container">
                <div className="row justify-content-center mb-4">
                    <div className="col-md-7 text-center">
                        <h1 className="mb-3">Experienced & Professional Team</h1>
                    </div>
                </div>
                <div className="row justify-content-around">
                    <div className="col-lg-4 mb-4">
                        <div className="row">
                            <div className="col-md-12">
                                <img src={avatar_alexkay} alt="AlexKay avatar" className="img-fluid rounded-circle" />
                            </div>
                            <div className="col-md-12 text-center">
                                <div className="pt-2">
                                    <h5 className="mt-4 font-weight-medium mb-0">Alexander Kaigorodov</h5>
                                    <h6 className="subtitle mb-3">DS / MLOps / NLP engineer</h6>
                                    <p>The project for the most brutal and effective language learning technique.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-lg-4 mb-4">
                        <div className="row">
                            <div className="col-md-12">
                                <img src={avatar_alkhimovmv} alt="Alkhimovmv avatar" className="img-fluid rounded-circle" />
                            </div>
                            <div className="col-md-12 text-center">
                                <div className="pt-2">
                                    <h5 className="mt-4 font-weight-medium mb-0">Maxim Alkhimov</h5>
                                    <h6 className="subtitle mb-3">Frontend Developer</h6>
                                    <p>A year from now you will wish you had started to learn a language today.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OurTeam;