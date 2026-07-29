// import ResumeSection from "./ResumeSection";

// interface Props {
//   resume: any;
// }

// export default function ResumeRenderer({ resume }: Props) {
//   if (!resume) {
//     return null;
//   }

//   return (
//     <div
//       className="
//    bg-white
//    border
//    shadow-xl
//    rounded-xl
//    p-10
//    text-sm
//    leading-6
//    h-full
//  "
//     >
//       {/* Header */}

//       <div className="text-center mb-6">
//         <h1 className="text-3xl font-bold tracking-wide">{resume.name}</h1>

//         <p className="text-gray-600 mt-2 font-medium">{resume.headline}</p>

//         <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
//           <span>{resume.contact_info?.location}</span>
//           <span>|</span>
//           <span>{resume.contact_info?.phone}</span>
//           <span>|</span>
//           <span>{resume.contact_info?.email}</span>
//         </div>
//       </div>

//       <ResumeSection title="Professional Summary">
//         <p className="text-gray-700">{resume.professional_summary?.content}</p>
//       </ResumeSection>

//       <ResumeSection title="Technical Skills">
//         <div className="space-y-2">
//           {resume.technical_skills?.categories?.map((category: any) => (
//             <div key={category.category}>
//               <span className="font-semibold">{category.category}:</span>

//               <span className="ml-2 text-gray-700">
//                 {category.skills.join(", ")}
//               </span>
//             </div>
//           ))}
//         </div>
//       </ResumeSection>

//       <ResumeSection title="Professional Experience">
//         {resume.professional_experience?.map((exp: any, index: number) => (
//           <div key={index} className="mb-8">
//             <div className="flex justify-between items-start">
//               <div>
//                 <h3 className="font-bold text-base">{exp.role}</h3>

//                 <div className="text-gray-600">{exp.company}</div>
//               </div>

//               <div className="text-gray-500 text-xs">
//                 {exp.start_date} - {exp.end_date}
//               </div>
//             </div>

//             <ul className="list-disc ml-5 mt-3 space-y-1">
//               {exp.responsibilities?.map((point: string, idx: number) => (
//                 <li key={idx}>{point}</li>
//               ))}
//             </ul>

//             {exp.projects?.length > 0 && (
//               <div className="mt-4 ml-2">
//                 {exp.projects.map((project: any, pIndex: number) => (
//                   <div key={pIndex} className="mb-4">
//                     <h4 className="font-semibold">{project.title}</h4>

//                     <ul className="list-disc ml-5 mt-1">
//                       {project.bullet_points?.map(
//                         (bullet: string, bulletIndex: number) => (
//                           <li key={bulletIndex}>{bullet}</li>
//                         ),
//                       )}
//                     </ul>
//                   </div>
//                 ))}
//               </div>
//             )}
//           </div>
//         ))}
//       </ResumeSection>

//       <ResumeSection title="Certifications">
//         <ul className="list-disc ml-5">
//           {resume.certifications?.map((cert: any, index: number) => (
//             <li key={index}>{cert.name}</li>
//           ))}
//         </ul>
//       </ResumeSection>

//       <ResumeSection title="Education">
//         {resume.education?.map((edu: any, index: number) => (
//           <div key={index} className="mb-2">
//             <div className="font-semibold">{edu.degree}</div>

//             <div>{edu.institution}</div>

//             <div className="text-gray-500 text-sm">
//               {edu.start_year} - {edu.end_year}
//             </div>
//           </div>
//         ))}
//       </ResumeSection>
//     </div>
//   );
// }

/** */

// import ResumeSection from "./ResumeSection";
// import HighlightText from "./HighlightText";
// import HighlightListItem from "./HighlightListItem";

// import {
//   compareText,
//   findMatchingExperience,
//   findMatchingProject,
// } from "../../utils/resumeDiff";

// interface Props {
//   resume: any;
//   originalResume?: any;
// }

// export default function ResumeRenderer({ resume, originalResume }: Props) {
//   if (!resume) return null;

//   const summaryStatus = compareText(
//     originalResume?.professional_summary?.content,
//     resume.professional_summary?.content,
//   );

//   return (
//     <div
//       className="
//         bg-white
//         border
//         shadow-xl
//         rounded-xl
//         p-10
//         text-sm
//         leading-6
//         h-full
//       "
//     >
//       {/* Header */}

//       <div className="text-center mb-6">
//         <h1 className="text-3xl font-bold tracking-wide">
//           <HighlightText
//             text={resume.name}
//             status={compareText(originalResume?.name, resume.name)}
//           />
//         </h1>

//         <p className="text-gray-600 mt-2 font-medium">
//           <HighlightText
//             text={resume.headline}
//             status={compareText(originalResume?.headline, resume.headline)}
//           />
//         </p>

//         <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
//           <span>
//             <HighlightText
//               text={resume.contact_info?.location}
//               status={compareText(
//                 originalResume?.contact_info?.location,
//                 resume.contact_info?.location,
//               )}
//             />
//           </span>

//           <span>|</span>

//           <span>
//             <HighlightText
//               text={resume.contact_info?.phone}
//               status={compareText(
//                 originalResume?.contact_info?.phone,
//                 resume.contact_info?.phone,
//               )}
//             />
//           </span>

//           <span>|</span>

//           <span>
//             <HighlightText
//               text={resume.contact_info?.email}
//               status={compareText(
//                 originalResume?.contact_info?.email,
//                 resume.contact_info?.email,
//               )}
//             />
//           </span>
//         </div>
//       </div>

//       <ResumeSection title="Professional Summary">
//         <HighlightText
//           text={resume.professional_summary?.content}
//           status={summaryStatus}
//         />
//       </ResumeSection>

//       <ResumeSection title="Technical Skills">
//         <div className="space-y-2">
//           {resume.technical_skills?.categories?.map((category: any) => {
//             const originalCategory =
//               originalResume?.technical_skills?.categories?.find(
//                 (c: any) => c.category === category.category,
//               );

//             return (
//               <div key={category.category}>
//                 <span className="font-semibold">{category.category}:</span>

//                 <div className="ml-4 mt-1">
//                   {category.skills.map((skill: string) => (
//                     <HighlightListItem
//                       key={skill}
//                       text={skill}
//                       status={compareText(
//                         originalCategory?.skills?.includes(skill) ? skill : "",
//                         skill,
//                       )}
//                     />
//                   ))}
//                 </div>
//               </div>
//             );
//           })}
//         </div>
//       </ResumeSection>
//       <ResumeSection title="Professional Experience">
//         {resume.professional_experience?.map((exp: any, index: number) => {
//           const originalExp = findMatchingExperience(
//             originalResume?.professional_experience,
//             exp,
//           );

//           return (
//             <div key={index} className="mb-8">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="font-bold text-base">
//                     <HighlightText
//                       text={exp.role}
//                       status={compareText(originalExp?.role, exp.role)}
//                     />
//                   </h3>

//                   <div className="text-gray-600">
//                     <HighlightText
//                       text={exp.company}
//                       status={compareText(originalExp?.company, exp.company)}
//                     />
//                   </div>
//                 </div>

//                 <div className="text-gray-500 text-xs">
//                   <HighlightText
//                     text={`${exp.start_date} - ${exp.end_date}`}
//                     status={compareText(
//                       `${originalExp?.start_date ?? ""} - ${originalExp?.end_date ?? ""}`,
//                       `${exp.start_date} - ${exp.end_date}`,
//                     )}
//                   />
//                 </div>
//               </div>

//               <ul className="list-disc ml-5 mt-3 space-y-1">
//                 {exp.responsibilities?.map((point: string, idx: number) => (
//                   <HighlightListItem
//                     key={idx}
//                     text={point}
//                     status={compareText(
//                       originalExp?.responsibilities?.find(
//                         (p: string) => p === point,
//                       ),
//                       point,
//                     )}
//                   />
//                 ))}
//               </ul>

//               {exp.projects?.length > 0 && (
//                 <div className="mt-4 ml-2">
//                   {exp.projects.map((project: any, pIndex: number) => {
//                     const originalProject = findMatchingProject(
//                       originalExp?.projects,
//                       project,
//                     );

//                     return (
//                       <div key={pIndex} className="mb-4">
//                         <h4 className="font-semibold">
//                           <HighlightText
//                             text={project.title}
//                             status={compareText(
//                               originalProject?.title,
//                               project.title,
//                             )}
//                           />
//                         </h4>

//                         <ul className="list-disc ml-5 mt-1">
//                           {project.bullet_points?.map(
//                             (bullet: string, bulletIndex: number) => (
//                               <HighlightListItem
//                                 key={bulletIndex}
//                                 text={bullet}
//                                 status={compareText(
//                                   originalProject?.bullet_points?.find(
//                                     (b: string) => b === bullet,
//                                   ),
//                                   bullet,
//                                 )}
//                               />
//                             ),
//                           )}
//                         </ul>
//                       </div>
//                     );
//                   })}
//                 </div>
//               )}
//             </div>
//           );
//         })}
//       </ResumeSection>
//       <ResumeSection title="Certifications">
//         <ul className="list-disc ml-5 space-y-1">
//           {resume.certifications?.map((cert: any, index: number) => {
//             const originalCert = originalResume?.certifications?.find(
//               (c: any) => c.name === cert.name,
//             );

//             return (
//               <HighlightListItem
//                 key={index}
//                 text={cert.name}
//                 status={compareText(originalCert?.name, cert.name)}
//               />
//             );
//           })}
//         </ul>
//       </ResumeSection>

//       <ResumeSection title="Education">
//         {resume.education?.map((edu: any, index: number) => {
//           const originalEdu = originalResume?.education?.find(
//             (e: any) =>
//               e.degree === edu.degree && e.institution === edu.institution,
//           );

//           return (
//             <div key={index} className="mb-4">
//               <div className="font-semibold">
//                 <HighlightText
//                   text={edu.degree}
//                   status={compareText(originalEdu?.degree, edu.degree)}
//                 />
//               </div>

//               <div>
//                 <HighlightText
//                   text={edu.institution}
//                   status={compareText(
//                     originalEdu?.institution,
//                     edu.institution,
//                   )}
//                 />
//               </div>

//               <div className="text-gray-500 text-sm">
//                 <HighlightText
//                   text={`${edu.start_year} - ${edu.end_year}`}
//                   status={compareText(
//                     `${originalEdu?.start_year ?? ""} - ${originalEdu?.end_year ?? ""}`,
//                     `${edu.start_year} - ${edu.end_year}`,
//                   )}
//                 />
//               </div>
//             </div>
//           );
//         })}
//       </ResumeSection>
//     </div>
//   );
// }

import ResumeSection from "./ResumeSection";
import HighlightText from "./HighlightText";
// import HighlightListItem from "./HighlightListItem";

// import {
//   compareText,
//   findMatchingExperience,
//   findMatchingProject,
// } from "../../utils/resumeDiff";

interface Props {
  resume: any;
  originalResume?: any;
}



export default function ResumeRenderer({
  resume,
  originalResume,
}: Props) {
  if (!resume) return null;

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
        <h1 className="text-3xl font-bold tracking-wide">
          <HighlightText
            original={originalResume?.name}
            current={resume.name}
          />
        </h1>

        <p className="text-gray-600 mt-2 font-medium">
          <HighlightText
            original={originalResume?.headline}
            current={resume.headline}
          />
        </p>

        <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
          <span>
            <HighlightText
              original={originalResume?.contact_info?.location}
              current={resume.contact_info?.location}
            />
          </span>

          <span>|</span>

          <span>
            <HighlightText
              original={originalResume?.contact_info?.phone}
              current={resume.contact_info?.phone}
            />
          </span>

          <span>|</span>

          <span>
            <HighlightText
              original={originalResume?.contact_info?.email}
              current={resume.contact_info?.email}
            />
          </span>
        </div>
      </div>

      <ResumeSection title="Professional Summary">
        <HighlightText
          original={originalResume?.professional_summary?.content}
          current={resume.professional_summary?.content}
        />
      </ResumeSection>

      <ResumeSection title="Technical Skills">
        <div className="space-y-2">
          {resume.technical_skills?.categories?.map(
            (category: any) => {
              const originalCategory =
                originalResume?.technical_skills?.categories?.find(
                  (c: any) =>
                    c.category === category.category,
                );

              return (
                <div key={category.category}>
                  <span className="font-semibold">
                    {category.category}:
                  </span>

                  <ul className="list-disc ml-6 mt-2 space-y-1">
                    {category.skills.map(
                      (skill: string) => (
                        <li key={skill}>
                          <HighlightText
                            original={originalCategory?.skills?.find(
                              (s: string) => s === skill,
                            )}
                            current={skill}
                          />
                        </li>
                      ),
                    )}
                  </ul>
                </div>
              );
            },
          )}
        </div>
      </ResumeSection>
      <ResumeSection title="Professional Experience">
        {resume.professional_experience?.map(
          (exp: any, index: number) => {
            const originalExp =
              originalResume?.professional_experience?.find(
                (e: any) =>
                  e.company === exp.company ||
                  e.role === exp.role,
              );

            return (
              <div key={index} className="mb-8">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-base">
                      <HighlightText
                        original={originalExp?.role}
                        current={exp.role}
                      />
                    </h3>

                    <div className="text-gray-600">
                      <HighlightText
                        original={originalExp?.company}
                        current={exp.company}
                      />
                    </div>
                  </div>

                  <div className="text-gray-500 text-xs">
                    <HighlightText
                      original={`${originalExp?.start_date ?? ""} - ${originalExp?.end_date ?? ""}`}
                      current={`${exp.start_date} - ${exp.end_date}`}
                    />
                  </div>
                </div>

                <ul className="list-disc ml-5 mt-3 space-y-2">
                  {exp.responsibilities?.map(
                    (point: string, idx: number) => (
                      <li key={idx}>
                        <HighlightText
                          original={
                            originalExp?.responsibilities?.[idx]
                          }
                          current={point}
                        />
                      </li>
                    ),
                  )}
                </ul>

                {exp.projects?.length > 0 && (
                  <div className="mt-5 ml-2">
                    {exp.projects.map(
                      (
                        project: any,
                        pIndex: number,
                      ) => {
                        const originalProject =
                          originalExp?.projects?.find(
                            (p: any) =>
                              p.title === project.title,
                          );

                        return (
                          <div
                            key={pIndex}
                            className="mb-5"
                          >
                            <h4 className="font-semibold">
                              <HighlightText
                                original={
                                  originalProject?.title
                                }
                                current={project.title}
                              />
                            </h4>

                            <ul className="list-disc ml-5 mt-2 space-y-1">
                              {project.bullet_points?.map(
                                (
                                  bullet: string,
                                  bulletIndex: number,
                                ) => (
                                  <li key={bulletIndex}>
                                    <HighlightText
                                      original={
                                        originalProject
                                          ?.bullet_points?.[
                                          bulletIndex
                                        ]
                                      }
                                      current={bullet}
                                    />
                                  </li>
                                ),
                              )}
                            </ul>
                          </div>
                        );
                      },
                    )}
                  </div>
                )}
              </div>
            );
          },
        )}
      </ResumeSection>
            <ResumeSection title="Certifications">
        <ul className="list-disc ml-5 space-y-2">
          {resume.certifications?.map(
            (cert: any, index: number) => {
              const originalCert =
                originalResume?.certifications?.find(
                  (c: any) =>
                    c.name === cert.name,
                );

              return (
                <li key={index}>
                  <HighlightText
                    original={originalCert?.name}
                    current={cert.name}
                  />
                </li>
              );
            },
          )}
        </ul>
      </ResumeSection>

      <ResumeSection title="Education">
        {resume.education?.map(
          (edu: any, index: number) => {
            const originalEdu =
              originalResume?.education?.find(
                (e: any) =>
                  e.degree === edu.degree ||
                  e.institution === edu.institution,
              );

            return (
              <div key={index} className="mb-5">
                <div className="font-semibold">
                  <HighlightText
                    original={originalEdu?.degree}
                    current={edu.degree}
                  />
                </div>

                <div>
                  <HighlightText
                    original={originalEdu?.institution}
                    current={edu.institution}
                  />
                </div>

                <div className="text-gray-500 text-sm">
                  <HighlightText
                    original={`${originalEdu?.start_year ?? ""} - ${originalEdu?.end_year ?? ""}`}
                    current={`${edu.start_year} - ${edu.end_year}`}
                  />
                </div>
              </div>
            );
          },
        )}
      </ResumeSection>
    </div>
  );
}