interface Props {
  resume: any;
}

export default function ResumePreviewMini({ resume }: Props) {
  if (!resume) return null;

  return (
    <div className="p-4 space-y-4 text-sm">
      <div>
        <div className="font-bold text-gray-900">{resume.name}</div>
        <div className="text-xs text-gray-500">{resume.headline}</div>
      </div>

      <div>
        <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">
          Skills
        </div>
        <div className="flex flex-wrap gap-1">
          {resume.technical_skills?.categories?.flatMap((c: any) => c.skills)
            .slice(0, 20)
            .map((s: string) => (
              <span key={s} className="text-[11px] bg-white border border-gray-200 rounded-full px-2 py-0.5">
                {s}
              </span>
            ))}
        </div>
      </div>

      <div>
        <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">
          Experience
        </div>
        <ul className="space-y-1">
          {resume.professional_experience?.map((exp: any, i: number) => (
            <li key={i} className="text-xs text-gray-600">
              <span className="font-medium text-gray-800">{exp.role}</span> — {exp.company}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}