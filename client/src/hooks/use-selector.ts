import { useSelector as reduxUseSelector } from "react-redux";
import type { TypedUseSelectorHook } from "react-redux";
import type { RootState } from "../redux";

export const useSelector: TypedUseSelectorHook<RootState> = reduxUseSelector;
