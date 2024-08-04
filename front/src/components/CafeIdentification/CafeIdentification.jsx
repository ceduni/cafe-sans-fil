import PropTypes from 'prop-types';
import {Cafe} from '@/models/cafe';
import './styles.css'

const CafeIdentification = ({ cafe }) => {
    //console.log(cafe);
  return (
    <>
        <h3 className="cafe-name">{cafe.name}</h3>
        <p className="bare cafe-location">
            {cafe.location.toString()}
        </p>
        <p className="bare">
            {cafe.description}
        </p>
        <div className="cafe-identification__header">
            <h3 className="title">Staff</h3>
            <button className="btn btn-email">
                <svg className="email-icon" stroke="currentColor" fill="currentColor" strokeWidth="0" viewBox="0 0 24 24" height="200px" width="200px" xmlns="http://www.w3.org/2000/svg"><path fill="none" d="M0 0h24v24H0z"></path><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"></path></svg>
            </button>
            <button className="btn btn-volunteer">Devenir bénévole</button>
        </div>
        <ul className="bare-list team-members">
            <li className="team-member">
                <img className="team-member-photo" src="https://nimblebar.co/wp-content/uploads/2021/04/DSC3375.jpg" />
                <h3 className="team-member-name">Jeremy</h3>
                <span className="team-member-role">Gérant</span>
            </li>
            <li className="team-member">
                <img className="team-member-photo" src="https://media.istockphoto.com/id/1404412754/photo/various-shakers-and-bottles-stand-on-the-bar-counter-and-bartender-gently-pours-alcoholic.jpg?s=612x612&w=0&k=20&c=_Stb_4zojqZ1LhfB8TFilaxso4vB19mM94gNEgJmgBA=" />
                <h3 className="team-member-name">Simon</h3>
                <span className="team-member-role">Gérant</span>
            </li>
            <li className="team-volunteer">
                <span className="num">54</span>  
                <span className="txt">bénévoles</span>
            </li>
        </ul>
    </>
)
};

CafeIdentification.propTypes = {
    cafe: PropTypes.instanceOf(Cafe).isRequired,
};

export default CafeIdentification;
