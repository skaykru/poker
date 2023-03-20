import { PropsWithChildren } from "react";
import "./menu-card.scss";

type MenuCardProps = {
  readonly title: string;
};

export const MenuCard = ({
  title,
  children,
}: PropsWithChildren<MenuCardProps>) => {
  return (
    <div className="menu-card">
      <h1>{title}</h1>
      {children}
    </div>
  );
};
