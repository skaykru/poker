import { Link } from "react-router-dom";
import { getGuestToken } from "../../api/user-api";
import { MenuCard } from "../../components/menu-card/menu-card";
import { setAccessToken } from "../../helpers/local-storage-helper";
import { useDispatch } from "../../hooks/use-dispatch";
import { fetchUserSucceeded } from "../../redux/slices/user-slice";
import "./welcome-page.scss";

export const WelcomePage = () => {
  const dispatch = useDispatch();

  const onPlayAsGuestClick = async () => {
    try {
      const { access_token } = await getGuestToken();
      setAccessToken(access_token);
      dispatch(fetchUserSucceeded({ type: "Guest" }));
    } catch (e) {
      console.error("Was not able to get guest token", e);
    }
  };

  return (
    <div className="welcome-page">
      <MenuCard title="Choose an account">
        <Link to="/login">
          <button className="login">Login</button>
        </Link>
        <Link to="/sign-up">
          <button className="sign-up">Sign Up</button>
        </Link>
        <button className="guest" onClick={onPlayAsGuestClick}>
          Play as guest
        </button>
      </MenuCard>
    </div>
  );
};
