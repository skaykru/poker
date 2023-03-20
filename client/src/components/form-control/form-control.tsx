import { ChangeEventHandler } from "react";
import "./form-control.scss";

type FormControlProps = {
  readonly name: string;
  readonly value: string;
  readonly label?: string;
  readonly type?: string;
  readonly width?: string;
  readonly marginTop?: string;
  readonly onChange: ChangeEventHandler<HTMLInputElement>;
};

export const FormControl = ({ label, name, value, onChange, marginTop, type = "text", width = "100%" }: FormControlProps) => {
  return (
    <div style={{ width: width, marginTop }} className="auth-form-control">
      {label && <label htmlFor={name}>{label}</label>}
      <input value={value} onChange={onChange} id={name} type={type} />
    </div>
  );
};
