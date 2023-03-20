import { useEffect } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { getCurrentUser } from "./api/user-api";
import { useDispatch } from "./hooks/use-dispatch";
import { useSelector } from "./hooks/use-selector";
import { JoinRoomPage } from "./pages/join-room-page/join-room-page";
import { LoadingPage } from "./pages/loading-page/loading-page";
import { LoginPage } from "./pages/login-page/login-page";
import { SignUpPage } from "./pages/sign-up-page/sign-up-page";
import { WelcomePage } from "./pages/welcome-page/welcome-page";
import { fetchUserSucceeded, fetchUserFailed } from "./redux/slices/user-slice";

export const App = () => {
  const dispatch = useDispatch();

  const isLoggedIn = useSelector((s) => s.user.isLoggedIn);
  const isLoading = useSelector((s) => s.user.isLoading);

  useEffect(() => {
    getCurrentUser()
      .then((res) => {
        dispatch(fetchUserSucceeded(res));
      })
      .catch((err) => {
        dispatch(fetchUserFailed());
        if (err.response?.status !== 401) console.error(err);
      });
  }, []);

  if (isLoading) return <LoadingPage />;

  return (
    <Routes>
      {!isLoggedIn ? (
        <>
          <Route path="/welcome" element={<WelcomePage />} />
          <Route path="/sign-up" element={<SignUpPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/welcome" />} />
        </>
      ) : (
        <>
          <Route path="/join-room" element={<JoinRoomPage />} />
          <Route path="*" element={<Navigate to="/join-room" />} />
        </>
      )}
    </Routes>
  );
};
