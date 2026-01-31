import { useAuth } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
    const { logout } = useAuth();

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <span className="navbar-logo">Scriptoria</span>
            </div>

            <div className="navbar-right">
                <button
                    className="logout-btn"
                    onClick={logout}
                >
                    LOGOUT
                </button>
            </div>
        </nav>
    );
}

export default Navbar;
