interface Props {
  title: string;
  value: string | number;
}

export default function ATSCard({ title, value }: Props) {
  return (
    <div className="bg-white border rounded-xl p-5 shadow-sm">
      {" "}
      <div className="text-sm text-gray-500 ">{title} </div>
     <div className="text-4xl font-bold ">{value}</div>
    </div>
  );
}
