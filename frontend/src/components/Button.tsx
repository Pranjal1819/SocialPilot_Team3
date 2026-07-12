"use client";

type ButtonProps = {
  text: string;
  type?: "button" | "submit";
  loading?: boolean;
};

export default function Button({
  text,
  type = "button",
  loading = false,
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={loading}
      className="
        w-full
        py-3.5
        rounded-xl
        text-white
        font-semibold
        tracking-wide
        transition-all
        duration-300
        hover:scale-[1.02]
        hover:-translate-y-0.5
        disabled:opacity-70
        disabled:cursor-not-allowed
      "
      style={{
        background: loading
          ? "#94A3B8"
          : "linear-gradient(135deg, #0096C7 0%, #0077B6 100%)",
        boxShadow: loading
          ? "none"
          : "0 12px 30px -10px rgba(0,119,182,0.4)",
      }}
    >
      {loading ? "Please wait..." : text}
    </button>
  );
}