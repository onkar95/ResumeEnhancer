import ResumeSection from "./ResumeSection";

interface Props {
  resume: any;
}

export default function ResumeRenderer({ resume }: Props) {
  if (!resume) {
    return null;
  }

  return (
    <div
      className="
   bg-white
   border
   shadow-xl
   rounded-xl
   p-10
   text-sm
   leading-6
   h-full
 "
    >
      {/* Header */}

      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold tracking-wide">{resume.name}</h1>

        <p className="text-gray-600 mt-2 font-medium">{resume.headline}</p>

        <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
          <span>{resume.contact_info?.location}</span>
          <span>|</span>
          <span>{resume.contact_info?.phone}</span>
          <span>|</span>
          <span>{resume.contact_info?.email}</span>
        </div>
      </div>

      <ResumeSection title="Professional Summary">
        <p className="text-gray-700">{resume.professional_summary?.content}</p>
      </ResumeSection>

      <ResumeSection title="Technical Skills">
        <div className="space-y-2">
          {resume.technical_skills?.categories?.map((category: any) => (
            <div key={category.category}>
              <span className="font-semibold">{category.category}:</span>

              <span className="ml-2 text-gray-700">
                {category.skills.join(", ")}
              </span>
            </div>
          ))}
        </div>
      </ResumeSection>

      <ResumeSection title="Professional Experience">
        {resume.professional_experience?.map((exp: any, index: number) => (
          <div key={index} className="mb-8">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-base">{exp.role}</h3>

                <div className="text-gray-600">{exp.company}</div>
              </div>

              <div className="text-gray-500 text-xs">
                {exp.start_date} - {exp.end_date}
              </div>
            </div>

            <ul className="list-disc ml-5 mt-3 space-y-1">
              {exp.responsibilities?.map((point: string, idx: number) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>

            {exp.projects?.length > 0 && (
              <div className="mt-4 ml-2">
                {exp.projects.map((project: any, pIndex: number) => (
                  <div key={pIndex} className="mb-4">
                    <h4 className="font-semibold">{project.title}</h4>

                    <ul className="list-disc ml-5 mt-1">
                      {project.bullet_points?.map(
                        (bullet: string, bulletIndex: number) => (
                          <li key={bulletIndex}>{bullet}</li>
                        ),
                      )}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </ResumeSection>

      <ResumeSection title="Certifications">
        <ul className="list-disc ml-5">
          {resume.certifications?.map((cert: any, index: number) => (
            <li key={index}>{cert.name}</li>
          ))}
        </ul>
      </ResumeSection>

      <ResumeSection title="Education">
        {resume.education?.map((edu: any, index: number) => (
          <div key={index} className="mb-2">
            <div className="font-semibold">{edu.degree}</div>

            <div>{edu.institution}</div>

            <div className="text-gray-500 text-sm">
              {edu.start_year} - {edu.end_year}
            </div>
          </div>
        ))}
      </ResumeSection>
    </div>
  );
}
