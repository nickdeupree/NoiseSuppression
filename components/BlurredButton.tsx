import { Button, ButtonProps } from "@heroui/button";

export function BlurredButton(props: ButtonProps) {
  return (
    <Button
      {...props}
      className={[
        "shadow-xl",
        "bg-default-200/50",
        "dark:bg-default/60",
        "backdrop-blur-xl",
        "backdrop-saturate-200",
        "hover:bg-default-200/70",
        "dark:hover:bg-default/70",
        "group-data-[focus=true]:bg-default-200/50",
        "dark:group-data-[focus=true]:bg-default/60",
        props.className,
      ].join(" ")}
    >
      {props.children}
    </Button>
  );
}
