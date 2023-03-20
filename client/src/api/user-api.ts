import axios from "axios";
import { getAccessToken } from "../helpers/local-storage-helper";

type TokenResponse = {
  readonly access_token: string;
  readonly refresh_token: string;
};

type UserResponse = TokenResponse & {
  readonly username: string;
  readonly email: string;
};

type GetCurrentUserResponse = {
  readonly type: "Guest" | "User";
  readonly email?: string;
  readonly nickname?: string;
};

export const login = async (
  email: string,
  password: string
): Promise<UserResponse> => {
  const res = await axios.post<UserResponse>(
    "http://localhost:8000/user/login",
    {
      email,
      password,
    }
  );
  return res.data;
};

export const signUp = async (
  email: string,
  password: string,
  username: string
): Promise<UserResponse> => {
  const res = await axios.post<UserResponse>(
    "http://localhost:8000/user/sign_up",
    {
      email,
      username,
      password,
    }
  );
  return res.data;
};

export const getGuestToken = async (): Promise<TokenResponse> => {
  const res = await axios.post<TokenResponse>(
    "http://localhost:8000/user/sign_up_guest"
  );
  return res.data;
};

export const getCurrentUser = async (): Promise<GetCurrentUserResponse> => {
  const res = await axios.get(
    `http://localhost:8000/user/get_current_player?token=${getAccessToken()}`
  );
  return res.data;
};
