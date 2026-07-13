interface Props {
  gapAnalysis: any;
}

export default function GapAnalysis({ gapAnalysis }: Props) {
  if (!gapAnalysis) return null;

  return (
    <div className="bg-white rounded-xl p-6 shadow">
      {" "}
      <h2 className="text-xl font-bold mb-4">Gap Analysis </h2>
      <div className="mb-4">
        <h3 className="font-semibold mb-2">Missing Skills</h3>

        <div className="flex flex-wrap gap-2">
          {gapAnalysis.missing_skills?.map((skill: string) => (
            <span
              key={skill}
              className="bg-red-100 text-red-700 px-3 py-1 rounded-full"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>
      <div>
        <h3 className="font-semibold mb-2">Matched Skills</h3>

        <div className="flex flex-wrap gap-2">
          {gapAnalysis.already_present?.map((skill: string) => (
            <span
              key={skill}
              className="bg-green-100 text-green-700 px-3 py-1 rounded-full"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
