import * as React from "react";
import { cn } from "@/lib/utils";

export function ButtonGroup({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      className={cn(
        "inline-flex items-center [&>*]:rounded-none [&>*:first-child]:rounded-l-xl [&>*:last-child]:rounded-r-xl [&>*:not(:first-child)]:-ml-px",
        className
      )}
      {...props}
    />
  );
}