import * as React from "react";
import { cn } from "@/lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "h-11 w-full rounded-xl border border-gray-300 bg-white px-3.5 text-sm text-slate-900 outline-none transition duration-200 placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/25 disabled:cursor-not-allowed disabled:opacity-60",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";

export { Input };
