interface CampaignFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export default function CampaignFilter({
  value,
  onChange,
}: CampaignFilterProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-lg border p-3 outline-none focus:border-blue-500"
    >
      <option value="All">All</option>
      <option value="Running">Running</option>
      <option value="Completed">Completed</option>
      <option value="Draft">Draft</option>
      <option value="Paused">Paused</option>
    </select>
  );
}