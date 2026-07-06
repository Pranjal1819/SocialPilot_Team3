"use client";

type ButtonProps = {
  text: string;
  type?: "button" | "submit";
};

export default function Button({
  text,
  type = "button",
}: ButtonProps) {
  return (
    <button
      type={type}
      className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
    >
      {text}
    </button>
  );
}