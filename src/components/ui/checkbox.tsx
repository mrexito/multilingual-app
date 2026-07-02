import * as React from "react";
import { cn } from "@/lib/utils";

const Checkbox = React.forwardRef<
  HTMLInputElement,
  React.ComponentProps<"input">
>(({ className, ...props }, ref) => {
  return (
    <label className="flex items-center space-x-2 text-sm">
      <input
        type="checkbox"
        className={cn(
          "h-4 w-4 rounded-sm border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-2",
          className
        )}
        ref={ref}
        {...props}
      />
      <span className="text-muted-foreground text-[#ACB1BC]">
        Remember for 30 days
      </span>
    </label>
  );
});

Checkbox.displayName = "Checkbox";

export { Checkbox };
