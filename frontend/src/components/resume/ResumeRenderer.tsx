import ResumeSection from "./ResumeSection";
import HighlightText from "./HighlightText";

interface Props {
  resume: any;
  originalResume?: any;
  /** Only true for the tailored draft. Original resume never diffs. */
  diff?: boolean;
}

export default function ResumeRenderer({
  resume,
  originalResume,
  diff = false,
}: Props) {
  if (!resume) return null;

  return (
    <div className="bg-white border shadow-xl rounded-xl p-10 text-sm leading-6 h-full">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold tracking-wide">
          <HighlightText diff={diff} original={originalResume?.name} current={resume.name} />
        </h1>

        <p className="text-gray-600 mt-2 font-medium">
          <HighlightText diff={diff} original={originalResume?.headline} current={resume.headline} />
        </p>

        <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
          <span>
            <HighlightText
              diff={diff}
              original={originalResume?.contact_info?.location}
              current={resume.contact_info?.location}
            />
          </span>
          <span>|</span>
          <span>
            <HighlightText
              diff={diff}
              original={originalResume?.contact_info?.phone}
              current={resume.contact_info?.phone}
            />
          </span>
          <span>|</span>
          <span>
            <HighlightText
              diff={diff}
              original={originalResume?.contact_info?.email}
              current={resume.contact_info?.email}
            />
          </span>
        </div>
      </div>

      <ResumeSection title="Professional Summary">
        <HighlightText
          diff={diff}
          original={originalResume?.professional_summary?.content}
          current={resume.professional_summary?.content}
        />
      </ResumeSection>

      <ResumeSection title="Technical Skills">
        <div className="space-y-2">
          {resume.technical_skills?.categories?.map((category: any) => {
            const originalCategory = originalResume?.technical_skills?.categories?.find(
              (c: any) => c.category === category.category,
            );

            return (
              <div key={category.category}>
                <span className="font-semibold">{category.category}:</span>
                <ul className="list-disc ml-6 mt-2 space-y-1">
                  {category.skills.map((skill: string) => (
                    <li key={skill}>
                      <HighlightText
                        diff={diff}
                        original={originalCategory?.skills?.find((s: string) => s === skill)}
                        current={skill}
                      />
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      </ResumeSection>

      <ResumeSection title="Professional Experience">
        {resume.professional_experience?.map((exp: any, index: number) => {
          const originalExp = originalResume?.professional_experience?.find(
            (e: any) => e.company === exp.company || e.role === exp.role,
          );

          return (
            <div key={index} className="mb-8">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-base">
                    <HighlightText diff={diff} original={originalExp?.role} current={exp.role} />
                  </h3>
                  <div className="text-gray-600">
                    <HighlightText diff={diff} original={originalExp?.company} current={exp.company} />
                  </div>
                </div>

                <div className="text-gray-500 text-xs">
                  <HighlightText
                    diff={diff}
                    original={`${originalExp?.start_date ?? ""} - ${originalExp?.end_date ?? ""}`}
                    current={`${exp.start_date} - ${exp.end_date}`}
                  />
                </div>
              </div>

              <ul className="list-disc ml-5 mt-3 space-y-2">
                {exp.responsibilities?.map((point: string, idx: number) => (
                  <li key={idx}>
                    <HighlightText
                      diff={diff}
                      original={originalExp?.responsibilities?.[idx]}
                      current={point}
                    />
                  </li>
                ))}
              </ul>

              {exp.projects?.length > 0 && (
                <div className="mt-5 ml-2">
                  {exp.projects.map((project: any, pIndex: number) => {
                    const originalProject = originalExp?.projects?.find(
                      (p: any) => p.title === project.title,
                    );

                    return (
                      <div key={pIndex} className="mb-5">
                        <h4 className="font-semibold">
                          <HighlightText
                            diff={diff}
                            original={originalProject?.title}
                            current={project.title}
                          />
                        </h4>

                        <ul className="list-disc ml-5 mt-2 space-y-1">
                          {project.bullet_points?.map((bullet: string, bulletIndex: number) => (
                            <li key={bulletIndex}>
                              <HighlightText
                                diff={diff}
                                original={originalProject?.bullet_points?.[bulletIndex]}
                                current={bullet}
                              />
                            </li>
                          ))}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </ResumeSection>

      <ResumeSection title="Certifications">
        <ul className="list-disc ml-5 space-y-2">
          {resume.certifications?.map((cert: any, index: number) => {
            const originalCert = originalResume?.certifications?.find(
              (c: any) => c.name === cert.name,
            );

            return (
              <li key={index}>
                <HighlightText diff={diff} original={originalCert?.name} current={cert.name} />
              </li>
            );
          })}
        </ul>
      </ResumeSection>

      <ResumeSection title="Education">
        {resume.education?.map((edu: any, index: number) => {
          const originalEdu = originalResume?.education?.find(
            (e: any) => e.degree === edu.degree || e.institution === edu.institution,
          );

          return (
            <div key={index} className="mb-5">
              <div className="font-semibold">
                <HighlightText diff={diff} original={originalEdu?.degree} current={edu.degree} />
              </div>
              <div>
                <HighlightText
                  diff={diff}
                  original={originalEdu?.institution}
                  current={edu.institution}
                />
              </div>
              <div className="text-gray-500 text-sm">
                <HighlightText
                  diff={diff}
                  original={`${originalEdu?.start_year ?? ""} - ${originalEdu?.end_year ?? ""}`}
                  current={`${edu.start_year} - ${edu.end_year}`}
                />
              </div>
            </div>
          );
        })}
      </ResumeSection>
    </div>
  );
}