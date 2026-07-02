import * as React from "react";
import { cn } from "@/lib/utils";

type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

const LabeledInput = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, ...props }, ref) => {
    return (
      <div className="space-y-2">
        {label && (
          <label
            htmlFor={props.id}
            className="block text-sm font-medium text-[#ACB1BC]"
          >
            {label}
          </label>
        )}

        <input
          type={type}
          className={cn(
            "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-black text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
            error ? "border-red-600" : "border-input",
            className
          )}
          ref={ref}
          {...props}
        />

        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
    );
  }
);

LabeledInput.displayName = "LabeledInput";

export { LabeledInput };
