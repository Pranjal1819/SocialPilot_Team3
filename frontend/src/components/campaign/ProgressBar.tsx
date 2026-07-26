interface ProgressBarProps {
  value: number;
}

export default function ProgressBar({ value }: ProgressBarProps) {
  return (
    <div className="mt-5">
      <div className="h-3 w-full rounded-full bg-gray-200 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-blue-600 to-cyan-500 transition-all duration-500"
          style={{ width: `${value}%` }}
        />
      </div>

      <p className="mt-2 text-sm text-gray-500">
        {value}% Complete
      </p>
    </div>
  );
}