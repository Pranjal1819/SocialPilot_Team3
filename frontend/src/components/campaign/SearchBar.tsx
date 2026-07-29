interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export default function SearchBar({
  value,
  onChange,
}: SearchBarProps) {
  return (
    <input
      type="text"
      placeholder="Search campaigns..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-lg border p-3 outline-none focus:border-blue-500"
    />
  );
}