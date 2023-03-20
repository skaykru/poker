import { ChangeEventHandler, useState } from "react";
import isEmail from "validator/lib/isEmail";

type Requirements = {
  readonly isRequired?: boolean;
  readonly isEmail?: boolean;
};

const validate = (value: string, requirements?: Requirements): boolean => {
  if (!requirements) return true;

  let isValid = true;

  if (requirements.isRequired && !value) {
    isValid = false;
  }

  if (requirements.isEmail && !isEmail(value)) {
    isValid = false;
  }

  return isValid;
};

export const useInput = (requirements?: Requirements) => {
  const [value, setValue] = useState<string>("");
  const [isValid, setIsValid] = useState<boolean>(validate("", requirements));
  const [isTouched, setIsTouched] = useState<boolean>(false);

  const onChange: ChangeEventHandler<HTMLInputElement> = (e) => {
    const value = e.target.value;
    setValue(value);
    setIsTouched(true);
    setIsValid(validate(value, requirements));
  };

  return { value, isValid, isTouched, onChange };
};
