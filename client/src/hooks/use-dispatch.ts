import { useDispatch as reduxUseDispatch } from "react-redux";
import type { AppDispatch } from "../redux";

export const useDispatch: () => AppDispatch = reduxUseDispatch;
