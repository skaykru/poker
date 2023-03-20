import { createSlice, PayloadAction } from "@reduxjs/toolkit";

type FetchUserSucceededPayload = {
  readonly type: "Guest" | "User";
  readonly email?: string;
  readonly username?: string;
};

export type UserState = {
  readonly type: "Guest" | "User" | null;
  readonly email: string | null;
  readonly username: string | null;
  readonly isLoggedIn: boolean;
  readonly isLoading: boolean;
};

const initialState: UserState = {
  type: null,
  email: null,
  username: null,
  isLoggedIn: false,
  isLoading: true,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    fetchUserSucceeded: (
      state,
      action: PayloadAction<FetchUserSucceededPayload>
    ) => {
      const { email = null, username = null, type } = action.payload;
      state.email = email;
      state.username = username;
      state.type = type;
      state.isLoggedIn = true;
      state.isLoading = false;
    },
    fetchUserFailed: (state) => {
      state.isLoading = false;
    },
    logout: () => initialState,
  },
});

export const { fetchUserSucceeded, fetchUserFailed, logout } =
  userSlice.actions;
export const userReducer = userSlice.reducer;
