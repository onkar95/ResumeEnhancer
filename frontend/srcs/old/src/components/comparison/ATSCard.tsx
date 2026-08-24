interface Props {
  title: string;
  value: string | number;
}

export default function ATSCard({ title, value }: Props) {
  return (
    <div className="card p-5 min-w-0">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-4xl font-bold text-brand-700 mt-1">{value}</div>
    </div>
  );
}