interface CampaignSortProps {
  value: string;
  onChange: (value: string) => void;
}

export default function CampaignSort({
  value,
  onChange,
}: CampaignSortProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-xl border border-gray-300 bg-white px-4 py-3 shadow-sm outline-none transition focus:border-blue-500"
    >
      <option value="default">Sort By</option>
      <option value="name">Campaign Name</option>
      <option value="budget">Budget</option>
      <option value="progress">Progress</option>
      <option value="status">Status</option>
    </select>
  );
}