import { FormEventHandler } from "react";
import { login } from "../../api/user-api";
import { MenuCard } from "../../components/menu-card/menu-card";
import { FormControl } from "../../components/form-control/form-control";
import { setAccessToken } from "../../helpers/local-storage-helper";
import { useDispatch } from "../../hooks/use-dispatch";
import { useInput } from "../../hooks/use-input";
import { fetchUserSucceeded } from "../../redux/slices/user-slice";
import "./login-page.scss";

export const LoginPage = () => {
  const dispatch = useDispatch();

  const emailInput = useInput({ isRequired: true, isEmail: true });
  const passwordInput = useInput({ isRequired: true });

  const btnClasses = [];
  if (emailInput.isValid && passwordInput.isValid) {
    btnClasses.push("valid");
  }

  const onSubmit: FormEventHandler = async (e) => {
    e.preventDefault();

    if (!emailInput.isValid || !passwordInput.isValid) {
      return;
    }

    try {
      const user = await login(emailInput.value, passwordInput.value);
      setAccessToken(user.access_token);
      dispatch(
        fetchUserSucceeded({
          type: "User",
          username: user.username,
          email: user.email,
        })
      );
    } catch (e) {
      console.error("Was not able to login", e);
    }
  };

  return (
    <div className="login-page">
      <MenuCard title="Login">
        <form onSubmit={onSubmit}>
          <FormControl
            value={emailInput.value}
            onChange={emailInput.onChange}
            name="email"
            type="email"
            label="Email"
          />
          <FormControl
            marginTop="10px"
            value={passwordInput.value}
            onChange={passwordInput.onChange}
            name="password"
            type="password"
            label="Password"
          />
          <button className={btnClasses.join(" ")}>Login</button>
        </form>
      </MenuCard>
    </div>
  );
};
