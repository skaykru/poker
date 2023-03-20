import { FormEventHandler } from "react";
import { signUp } from "../../api/user-api";
import { MenuCard } from "../../components/menu-card/menu-card";
import { FormControl } from "../../components/form-control/form-control";
import { setAccessToken } from "../../helpers/local-storage-helper";
import { useDispatch } from "../../hooks/use-dispatch";
import { useInput } from "../../hooks/use-input";
import { fetchUserSucceeded } from "../../redux/slices/user-slice";
import "./sign-up-page.scss";

export const SignUpPage = () => {
  const dispatch = useDispatch();

  const emailInput = useInput({ isRequired: true, isEmail: true });
  const nicknameInput = useInput({ isRequired: true });
  const passwordInput = useInput({ isRequired: true });

  const btnClasses = [];
  if (emailInput.isValid && nicknameInput.isValid && passwordInput.isValid) {
    btnClasses.push("valid");
  }

  const onSubmit: FormEventHandler = async (e) => {
    e.preventDefault();

    if (!emailInput.isValid || !nicknameInput.isValid || !passwordInput.isValid) {
      return;
    }

    try {
      const user = await signUp(emailInput.value, passwordInput.value, nicknameInput.value);
      setAccessToken(user.access_token);
      dispatch(
        fetchUserSucceeded({
          type: "User",
          username: user.username,
          email: user.email,
        })
      );
    } catch (e) {
      console.error("Was not able to sign up", e);
    }
  };

  return (
    <div className="sign-up-page">
      <MenuCard title="Sign Up">
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
            value={nicknameInput.value}
            onChange={nicknameInput.onChange}
            name="nickname"
            type="text"
            label="Nickname"
          />
          <FormControl
            marginTop="10px"
            value={passwordInput.value}
            onChange={passwordInput.onChange}
            name="password"
            type="password"
            label="Password"
          />
          <button className={btnClasses.join(" ")}>Sign Up</button>
        </form>
      </MenuCard>
    </div>
  );
};
