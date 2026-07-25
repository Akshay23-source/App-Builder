import * as React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl text-slate-100 shadow-xl",
      className
    )}
    {...props}
  />
));
Card.displayName = "Card";

export const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "default" | "outline" | "ghost" }
>(({ className, variant = "default", ...props }, ref) => {
  const baseStyle = "inline-flex items-center justify-center font-medium rounded-xl px-4 py-2.5 transition-all duration-200 focus:outline-none disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98]";
  const variants = {
    default: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/25 border border-indigo-400/30",
    outline: "border border-slate-700 hover:bg-slate-800 text-slate-200",
    ghost: "hover:bg-slate-800 text-slate-300",
  };
  return (
    <button
      ref={ref}
      className={cn(baseStyle, variants[variant], className)}
      {...props}
    />
  );
});
Button.displayName = "Button";

export function Badge({ children, className, variant = "indigo" }: { children: React.ReactNode; className?: string; variant?: "indigo" | "emerald" | "amber" | "slate" }) {
  const styles = {
    indigo: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
    emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    amber: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    slate: "bg-slate-800 text-slate-400 border-slate-700",
  };
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-semibold border", styles[variant], className)}>
      {children}
    </span>
  );
}
