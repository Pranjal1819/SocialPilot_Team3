type InputProps = {
  type: string;
  placeholder: string;
};

export default function Input({
  type,
  placeholder,
}: InputProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-600"
    />
  );
}